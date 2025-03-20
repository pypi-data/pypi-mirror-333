#include "mainwindow.hpp"
#include <QApplication>
#include <QFileDialog>
#include <QMessageBox>
#include <QProcess>
#include <QSettings>
#include <QToolButton>
#include <QVBoxLayout>
#include "apibridge.hpp"
#include "models/filesystem.hpp"
#include "views/dependencygraph.hpp"
#include "views/files.hpp"
#include "views/filesystem.hpp"
#include "views/loadingwidget.hpp"
#include "views/log.hpp"

namespace iprm {

MainWindow::MainWindow()
    : QMainWindow(nullptr),
      file_filter_(tr("IPRM Files (*.iprm);;All Files (*.*)")) {
  setup_api_bridge();
  setup_ui();
  create_actions();
  create_menu_bar();
  create_tool_bar();
  setWindowTitle(tr("IPRM Studio"));
  setWindowIcon(QIcon(":/logos/iprm_icon.svg"));
  resize(1280, 720);
  showMaximized();
}

void MainWindow::set_project_dir(const QDir& project_dir) {
  project_dir_ = project_dir;
  load_project();
}

void MainWindow::closeEvent(QCloseEvent* event) {
  QMainWindow::closeEvent(event);
  if (api_bridge_.isRunning()) {
    api_bridge_.destroy_sess();
    api_bridge_.quit();
    api_bridge_.wait();
  }
}

void MainWindow::setup_api_bridge() {
  auto bridge = &api_bridge_;
  // TODO: Fix up error handling to not assume all returned errors are project
  //  load failures
  connect(bridge, &APIBridgeThread::error, this,
          &MainWindow::on_project_load_failed);
  connect(bridge, &APIBridgeThread::print_stdout, this,
          &MainWindow::on_print_stdout);
  connect(bridge, &APIBridgeThread::project_load_success, this,
          &MainWindow::on_project_loaded);
  connect(bridge, &APIBridgeThread::cmake_generate_success, this,
          &MainWindow::on_cmake_generated);
  api_bridge_.start();
  QMetaObject::invokeMethod(bridge, &APIBridgeThread::capture_io,
                            Qt::QueuedConnection);
}

void MainWindow::setup_ui() {
  // Status Bar Setup
  status_bar_ = statusBar();
  auto progress_widget = new QWidget(this);
  auto progress_layout = new QHBoxLayout(progress_widget);
  progress_layout->setContentsMargins(0, 0, 0, 0);
  progress_layout->setSpacing(10);

  status_label_ = new QLabel(this);
  progress_bar_ = new QProgressBar(this);
  progress_bar_->setMaximumWidth(200);
  progress_bar_->setMaximumHeight(15);
  progress_bar_->setTextVisible(false);
  progress_bar_->hide();

  progress_layout->addWidget(status_label_);
  progress_layout->addWidget(progress_bar_);
  status_bar_->addWidget(progress_widget);

  // Log View
  log_view_ = new views::Log(project_dir_, this);
  log_dock_ = new QDockWidget(tr("Log"));
  log_dock_->setObjectName("log_dock");
  log_dock_->setWidget(log_view_);
  addDockWidget(Qt::BottomDockWidgetArea, log_dock_);
  connect(log_view_, &views::Log::process_started, this,
          &MainWindow::handle_process_started);
  connect(log_view_, &views::Log::process_finished, this,
          &MainWindow::handle_process_finished);
  connect(log_view_, &views::Log::process_error, this,
          &MainWindow::handle_process_error);
  log_view_->log("Welcome to IPRM Studio!");

  // File System View
  fs_model_ = new iprm::models::FileSystem(this);
  fs_view_ = new iprm::views::FileSystem(this);
  fs_view_->setModel(fs_model_);
  connect(fs_view_, &iprm::views::FileSystem::file_activated, this,
          &MainWindow::on_file_activated);
  fs_dock_ = new QDockWidget(tr("Project Files"));
  fs_dock_->setObjectName("fs_dock");
  fs_dock_->setWidget(fs_view_);

  // Dependency Graph View
  dep_view_ = new views::DependencyView(this);
  dep_dock_ = new QDockWidget(tr("Dependency Graph"));
  dep_dock_->setObjectName("dep_dock");
  dep_dock_->setWidget(dep_view_);

  // Project File View
  proj_file_view_ = new QStackedWidget(this);
  files_view_ = new views::Files(this);
  proj_file_view_->addWidget(files_view_);
  auto no_file_layout = new QVBoxLayout;
  no_file_layout->setAlignment(Qt::AlignCenter);
  auto no_file_label = new QLabel(tr("Select a File"), this);
  no_file_layout->addWidget(no_file_label);
  no_file_view_ = new QWidget(this);
  no_file_view_->setLayout(no_file_layout);
  connect(files_view_, &views::Files::file_closed, this,
          [this](const int num_files_opened) {
            if (num_files_opened <= 0) {
              proj_file_view_->setCurrentWidget(no_file_view_);
            }
          });
  proj_file_view_->addWidget(no_file_view_);
  proj_file_view_->setCurrentWidget(no_file_view_);

  // Main View
  auto no_proj_layout = new QVBoxLayout;
  no_proj_layout->setAlignment(Qt::AlignCenter);
  auto no_proj_label = new QLabel(tr("Open a Project"), this);
  no_proj_layout->addWidget(no_proj_label);
  no_proj_view_ = new QWidget(this);
  no_proj_view_->setLayout(no_proj_layout);

  auto loading_proj_failed_layout = new QHBoxLayout;
  loading_proj_failed_layout->setAlignment(Qt::AlignCenter);
  auto err_label_icon = new QLabel();
  err_label_icon->setPixmap(
      style()->standardIcon(QStyle::SP_MessageBoxCritical).pixmap(16, 16));
  auto err_label_msg =
      new QLabel(tr("Failed to load project. See Log window for more details"));
  loading_proj_failed_layout->addWidget(err_label_icon);
  loading_proj_failed_layout->addWidget(err_label_msg);
  loading_proj_failed_view_ = new QWidget(this);
  loading_proj_failed_view_->setLayout(loading_proj_failed_layout);

  loading_proj_view_ = new views::LoadingWidget(this);
  loading_proj_view_->set_text(tr("Loading Project..."));

  stack_ = new QStackedWidget(this);
  stack_->addWidget(no_proj_view_);
  stack_->addWidget(proj_file_view_);
  stack_->addWidget(loading_proj_failed_view_);
  stack_->addWidget(loading_proj_view_);
  stack_->setCurrentWidget(no_proj_view_);
  setCentralWidget(stack_);
}

void MainWindow::create_actions() {
  new_action_ = new QAction(QIcon::fromTheme("document-new"), tr("&New"), this);
  new_action_->setShortcut(QKeySequence::New);
  new_action_->setToolTip(tr("Create a new project"));
  connect(new_action_, &QAction::triggered, this, &MainWindow::new_project);

  open_action_ =
      new QAction(QIcon::fromTheme("document-open"), tr("&Open..."), this);
  open_action_->setShortcut(QKeySequence::Open);
  open_action_->setToolTip(tr("Open an existing project"));
  connect(open_action_, &QAction::triggered, this, &MainWindow::open_project);

  save_action_ =
      new QAction(QIcon::fromTheme("document-save"), tr("&Save"), this);
  save_action_->setShortcut(QKeySequence::Save);
  save_action_->setToolTip(tr("Save the current file"));
  connect(save_action_, &QAction::triggered, this,
          &MainWindow::save_current_file);

  save_as_action_ = new QAction(QIcon::fromTheme("document-save-as"),
                                tr("Save &As..."), this);
  save_as_action_->setShortcut(QKeySequence::SaveAs);
  save_as_action_->setToolTip(tr("Save the current file under a new name"));
  connect(save_as_action_, &QAction::triggered, this,
          &MainWindow::save_file_as);

  // TODO: Get icons that work with generate, configure, build ,test AND then
  //  import for the loaders
  cmake_generate_action_ =
      new QAction(QIcon::fromTheme("generate"), tr("Generate"), this);
  cmake_generate_action_->setToolTip(tr("Generate CMakeLists.txt Project"));
  connect(cmake_generate_action_, &QAction::triggered, this,
          &MainWindow::run_cmake_generate);

  cmake_configure_action_ =
      new QAction(QIcon::fromTheme("configure"), tr("Configure"), this);
  cmake_configure_action_->setToolTip(tr("Run CMake Configure"));
  connect(cmake_configure_action_, &QAction::triggered, this,
          &MainWindow::run_cmake_configure);

  cmake_build_action_ =
      new QAction(QIcon::fromTheme("build"), tr("Build"), this);
  cmake_build_action_->setToolTip(tr("Run CMake Build"));
  connect(cmake_build_action_, &QAction::triggered, this,
          &MainWindow::run_cmake_build);

  cmake_test_action_ = new QAction(QIcon::fromTheme("test"), tr("Test"), this);
  cmake_test_action_->setToolTip(tr("Run CMake Test"));
  connect(cmake_test_action_, &QAction::triggered, this,
          &MainWindow::run_cmake_test);

  scons_import_action_ =
      new QAction(QIcon::fromTheme("import"), tr("Import"), this);
  scons_import_action_->setToolTip(tr("Import SCons Project"));
  connect(scons_import_action_, &QAction::triggered, this,
          &MainWindow::on_scons_import);

  msbuild_import_action_ =
      new QAction(QIcon::fromTheme("import"), tr("Import"), this);
  msbuild_import_action_->setToolTip(tr("Import MSBuild Project"));
  connect(msbuild_import_action_, &QAction::triggered, this,
          &MainWindow::on_msbuild_import);
}

void MainWindow::create_menu_bar() {
  auto menu_bar = this->menuBar();

  auto file_menu = menu_bar->addMenu(tr("&File"));
  file_menu->addAction(new_action_);
  file_menu->addAction(open_action_);
  file_menu->addAction(save_action_);
  file_menu->addAction(save_as_action_);
  file_menu->addSeparator();
}

void MainWindow::create_tool_bar() {
  auto toolbar = new QToolBar(this);
  toolbar->setObjectName("toolbar");
  toolbar->setIconSize(QSize(16, 16));
  addToolBar(toolbar);

  toolbar->addAction(new_action_);
  toolbar->addAction(open_action_);
  toolbar->addAction(save_action_);
  toolbar->addAction(save_as_action_);
  toolbar->addSeparator();

  auto loaders_label = new QLabel(tr("Loaders"));
  auto loaders = new QWidget();
  auto loaders_layout = new QHBoxLayout(loaders);
  loaders_layout->setAlignment(Qt::AlignCenter);
  loaders_layout->setContentsMargins(0, 0, 0, 0);
  loaders_layout->addWidget(loaders_label);
  toolbar->addWidget(loaders);
  toolbar->addSeparator();

  auto scons_menu = new QMenu(this);
  scons_menu->addAction(scons_import_action_);
  auto scons_button = new QToolButton(this);
  scons_button->setMenu(scons_menu);
  scons_button->setPopupMode(QToolButton::MenuButtonPopup);
  scons_button->setText(tr("SCons"));
  scons_button->setIcon(QIcon(":/logos/scons.png"));
  scons_button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
  toolbar->addWidget(scons_button);

  auto msbuild_menu = new QMenu(this);
  msbuild_menu->addAction(msbuild_import_action_);
  auto msbuild_button = new QToolButton(this);
  msbuild_button->setMenu(msbuild_menu);
  msbuild_button->setPopupMode(QToolButton::MenuButtonPopup);
  msbuild_button->setText(tr("MSBuild"));
  msbuild_button->setIcon(QIcon(":/logos/msbuild.svg"));
  msbuild_button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
  toolbar->addWidget(msbuild_button);
  toolbar->addSeparator();

  auto generators_label = new QLabel(tr("Generators"));
  auto generators = new QWidget();
  auto generators_layout = new QHBoxLayout(generators);
  generators_layout->setAlignment(Qt::AlignCenter);
  generators_layout->setContentsMargins(0, 0, 0, 0);
  generators_layout->addWidget(generators_label);
  toolbar->addWidget(generators);
  toolbar->addSeparator();

  auto cmake_menu = new QMenu(this);
  cmake_menu->addAction(cmake_generate_action_);
  cmake_menu->addAction(cmake_configure_action_);
  cmake_menu->addAction(cmake_build_action_);
  cmake_menu->addAction(cmake_test_action_);
  auto cmake_button = new QToolButton(this);
  cmake_button->setMenu(cmake_menu);
  cmake_button->setPopupMode(QToolButton::MenuButtonPopup);
  cmake_button->setText(tr("CMake"));
  cmake_button->setIcon(QIcon(":/logos/cmake.svg"));
  cmake_button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
  toolbar->addWidget(cmake_button);
}

void MainWindow::disable_actions() {
  new_action_->setEnabled(false);
  open_action_->setEnabled(false);
  save_action_->setEnabled(false);
  save_as_action_->setEnabled(false);
  cmake_generate_action_->setEnabled(false);
  cmake_configure_action_->setEnabled(false);
  cmake_build_action_->setEnabled(false);
  cmake_test_action_->setEnabled(false);
  scons_import_action_->setEnabled(false);
  msbuild_import_action_->setEnabled(false);
}

void MainWindow::enable_actions() {
  new_action_->setEnabled(true);
  open_action_->setEnabled(true);
  save_action_->setEnabled(true);
  save_as_action_->setEnabled(true);
  cmake_generate_action_->setEnabled(true);
  cmake_configure_action_->setEnabled(true);
  cmake_build_action_->setEnabled(true);
  cmake_test_action_->setEnabled(true);
  scons_import_action_->setEnabled(true);
  msbuild_import_action_->setEnabled(true);
}

void MainWindow::load_project() {
  project_loaded_ = false;
  disable_actions();
  stack_->setCurrentWidget(loading_proj_view_);
  removeDockWidget(fs_dock_);
  removeDockWidget(dep_dock_);
  log_view_->start_logging_section("[Opening Project]");
  log_view_->log(QString("Loading project directory '%0'...")
                     .arg(project_dir_.absolutePath()));
  api_bridge_.set_root_dir(project_dir_);
  QMetaObject::invokeMethod(&api_bridge_, &APIBridgeThread::load_project,
                            Qt::QueuedConnection);
}

void MainWindow::on_project_loaded() {
  const auto& objects = api_bridge_.objects();
  std::vector<std::filesystem::path> file_paths;
  for (const auto& [path, _] : objects) {
    file_paths.push_back(std::filesystem::path(path));
  }
  fs_model_->load_tree(file_paths,
                       project_dir_.absolutePath().toLatin1().data());

  addDockWidget(Qt::LeftDockWidgetArea, fs_dock_);
  addDockWidget(Qt::RightDockWidgetArea, dep_dock_);
  resizeDocks({fs_dock_, dep_dock_}, {width() / 6, width() / 2},
              Qt::Orientation::Horizontal);

  fs_dock_->show();
  dep_dock_->show();
  files_view_->set_project_objects(objects);
  dep_view_->build_graph(api_bridge_.dependency_graph(),
                         api_bridge_.dependency_node_data());

  enable_actions();
  stack_->setCurrentWidget(proj_file_view_);
  // We're ready, let it rip!
  log_view_->log(QString("\nProject directory '%0' loaded!")
                     .arg(project_dir_.absolutePath()),
                 views::Log::Type::Success);
  project_loaded_ = true;
  Q_EMIT ready();
}

void MainWindow::on_project_load_failed(const APIError& error) {
  // TODO: Setup error state, prompt user to re-try opening their folder, or
  //  opening a different one. Also ensure the log window is shown so they can
  //  see the errors that occurred during load
  enable_actions();
  log_view_->log_api_error(error);
  stack_->setCurrentWidget(loading_proj_failed_view_);
  Q_EMIT ready();
}

void MainWindow::on_cmake_generated() {
  log_view_->log(QString("CMake project generated for '%0'!")
                     .arg(project_dir_.absolutePath()),
                 views::Log::Type::Success);
}

void MainWindow::on_print_stdout(const QString& message) {
  log_view_->log(message);
}

void MainWindow::on_file_activated(const models::FileNode& file_node) {
  files_view_->add_file(file_node);
  proj_file_view_->setCurrentWidget(files_view_);
}

void MainWindow::on_file_modified(bool modified) {
  save_action_->setEnabled(modified);
}

void MainWindow::save_current_file() {
  // TODO: Implement
}

void MainWindow::save_file_as() {
  // TODO: Implement
}

void MainWindow::new_project() {
  // TODO: Implement
}

void MainWindow::open_project() {
  QString dir = QFileDialog::getExistingDirectory(
      this, tr("Open IPRM Project"), QDir::homePath(),
      QFileDialog::ShowDirsOnly | QFileDialog::DontResolveSymlinks);

  if (!dir.isEmpty()) {
    project_dir_ = QDir(dir);
    load_project();
  }
}

void MainWindow::run_cmake_generate() {
  log_view_->start_logging_section("[CMake Generate]");
  QMetaObject::invokeMethod(&api_bridge_, &APIBridgeThread::cmake_generate,
                            Qt::QueuedConnection);
}

void MainWindow::run_cmake_configure() {
  QDir build_dir(project_dir_.absoluteFilePath("build"));
  // TODO: Optionally allow ability to delete build directory and start clean
  /*
  if (build_dir.exists()) {
    // Remove build directory for reconfiguration
    if (!build_dir.removeRecursively()) {
      QMessageBox::warning(this, tr("Configure Error"),
                           tr("Failed to clean existing build directory"));
      return;
    }
  }
  */
  // TODO: Allow setting of CMake generator, don't hardcode to Ninja
  log_view_->start_logging_section("[CMake Configure]");
  log_view_->run_command("cmake",
                         {"-G", "Ninja", "-S", project_dir_.absolutePath(),
                          "-B", build_dir.absolutePath()},
                         project_dir_.absolutePath());
}

void MainWindow::run_cmake_build() {
  QDir build_dir(project_dir_.absoluteFilePath("build"));
  if (!build_dir.exists()) {
    QMessageBox::warning(this, tr("Build Error"),
                         tr("Build directory does not exist. Please configure "
                            "the project first."));
    return;
  }

  log_view_->start_logging_section("[CMake Build]");
  log_view_->run_command("cmake", {"--build", build_dir.absolutePath(),
                                   "--config", "Release", "--parallel"});
}

void MainWindow::run_cmake_test() {
  QDir build_dir(project_dir_.absoluteFilePath("build"));
  if (!build_dir.exists()) {
    QMessageBox::warning(this, tr("Test Error"),
                         tr("Build directory does not exist. Please configure "
                            "and build the project first."));
    return;
  }

  log_view_->start_logging_section("[CMake Test]");
  log_view_->run_command("ctest", {}, build_dir.absolutePath());
}

void MainWindow::handle_process_started(const QString& command) {
  if (!project_loaded_)
    return;

  progress_bar_->setRange(0, 0);  // Indeterminate progress
  progress_bar_->show();
  status_label_->setText(tr("Running: %1").arg(command));
}

void MainWindow::handle_process_finished(int exit_code,
                                         QProcess::ExitStatus exit_status) {
  if (!project_loaded_)
    return;

  progress_bar_->hide();
  if (exit_code == 0 && exit_status == QProcess::NormalExit) {
    status_label_->setText(tr("Command completed successfully"));
  } else {
    status_label_->setText(
        tr("Command failed with exit code %1").arg(exit_code));
  }

  QTimer::singleShot(2500, status_label_, &QLabel::clear);
}

void MainWindow::handle_process_error(QProcess::ProcessError error) {
  if (!project_loaded_)
    return;

  progress_bar_->hide();
  status_label_->setText(tr("Error: %1").arg(static_cast<int>(error)));
  QTimer::singleShot(2500, status_label_, &QLabel::clear);
}

void MainWindow::on_scons_import() {
  // TODO: Import scons impl
}

void MainWindow::on_msbuild_import() {
  // TODO: Import msbuild impl
}

}  // namespace iprm
