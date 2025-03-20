#pragma once

#include "apibridge.hpp"
#include "models/filesystem.hpp"

#include <QAction>
#include <QDir>
#include <QDockWidget>
#include <QLabel>
#include <QMainWindow>
#include <QMenuBar>
#include <QProcess>
#include <QProgressBar>
#include <QSize>
#include <QStackedWidget>
#include <QStatusBar>
#include <QString>
#include <QTimer>
#include <QToolBar>

#include <memory>

namespace iprm {

namespace models {
class FileSystem;
}  // namespace models

namespace views {
class FileSystem;
class DependencyView;
class Log;
class Files;
class LoadingWidget;
}  // namespace views

class Object;

class MainWindow : public QMainWindow {
  Q_OBJECT

 public:
  MainWindow();

  void set_project_dir(const QDir& project_dir);

 Q_SIGNALS:
  void ready();

 private Q_SLOTS:
  void on_project_load_failed(const APIError& error);
  void on_project_loaded();

  void on_cmake_generated();

  void on_print_stdout(const QString& message);

  void on_file_activated(const models::FileNode& file_node);
  void on_file_modified(bool modified);
  void save_current_file();
  void save_file_as();

  void new_project();
  void open_project();

  void run_cmake_generate();
  void run_cmake_configure();
  void run_cmake_build();
  void run_cmake_test();
  void handle_process_started(const QString& command);
  void handle_process_finished(int exit_code, QProcess::ExitStatus exit_status);
  void handle_process_error(QProcess::ProcessError error);

  void on_scons_import();

  void on_msbuild_import();

 protected:
  void closeEvent(QCloseEvent* event) override;

 private:
  void create_actions();
  void create_menu_bar();
  void create_tool_bar();
  void disable_actions();
  void enable_actions();
  void setup_ui();
  void setup_api_bridge();
  void load_project();

 private:
  QDir project_dir_;
  bool project_loaded_{false};
  QString file_filter_;

  APIBridgeThread api_bridge_;

  views::Log* log_view_{nullptr};
  QDockWidget* log_dock_{nullptr};

  views::Files* files_view_{nullptr};

  models::FileSystem* fs_model_{nullptr};
  views::FileSystem* fs_view_{nullptr};
  QDockWidget* fs_dock_{nullptr};

  views::DependencyView* dep_view_{nullptr};
  QDockWidget* dep_dock_{nullptr};

  QStatusBar* status_bar_{nullptr};
  QLabel* status_label_{nullptr};
  QProgressBar* progress_bar_{nullptr};

  QStackedWidget* stack_{nullptr};
  QStackedWidget* proj_file_view_{nullptr};
  QWidget* no_file_view_{nullptr};

  QWidget* no_proj_view_{nullptr};
  views::LoadingWidget* loading_proj_view_{nullptr};
  QWidget* loading_proj_failed_view_{nullptr};

  QAction* save_action_{nullptr};
  QAction* save_as_action_{nullptr};

  QAction* new_action_{nullptr};
  QAction* open_action_{nullptr};

  QAction* cmake_generate_action_{nullptr};
  QAction* cmake_configure_action_{nullptr};
  QAction* cmake_build_action_{nullptr};
  QAction* cmake_test_action_{nullptr};

  QAction* scons_import_action_{nullptr};
  QAction* msbuild_import_action_{nullptr};
};

}  // namespace iprm
