#pragma once

#include "../apibridge.hpp"
#include "../models/filesystem.hpp"
#include "../models/objects.hpp"

#include <QFileInfo>
#include <QHash>
#include <QItemSelection>
#include <QTabWidget>

class QTabWidget;

namespace iprm::views {

class NativeText;
class CMakeText;
class Objects;

class FileNode : public QWidget {
  Q_OBJECT
 public:
  FileNode(const QString& title,
           const QString& contents,
           const std::vector<ObjectNode>& objects,
           QWidget* parent = nullptr);

  const QString& title() const { return title_; }

  void show_cmake(QString contents);

 private Q_SLOTS:
  void on_object_selection_changed(const QModelIndex& index);

 private:
  QString title_;
  Objects* objects_view_{nullptr};
  NativeText* native_text_view_{nullptr};
  QTabWidget* cmake_text_{nullptr};
  // TODO: This should be a QHash of platform to CMakeText instances that are
  //  in the tab widget, given Windows +WSL means we can have one scenario
  //  where there is more than 1 platform we can generate to on a single host
  CMakeText* cmake_text_view_{nullptr};
};

class Files : public QTabWidget {
  Q_OBJECT

 public:
  Files(QWidget* parent = nullptr);

  void set_project_objects(
      const std::unordered_map<std::string, std::vector<ObjectNode>>& objects);

  void add_file(const models::FileNode& file_node);

 Q_SIGNALS:
  void file_closed(const int num_files_opened);

 private Q_SLOTS:
  void on_file_tab_closed(const int tab_index);

 private:
  FileNode* add_native(const std::filesystem::path& file_path);
  void add_cmake(const models::CMakeFile& file_node);

  QHash<std::filesystem::path, FileNode*> open_files_;
  std::unordered_map<std::string, std::vector<ObjectNode>> project_objects_;
};

}  // namespace iprm::views
