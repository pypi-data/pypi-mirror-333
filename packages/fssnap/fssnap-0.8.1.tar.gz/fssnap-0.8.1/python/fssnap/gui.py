import os
import sys

from PySide6.QtCore import QSize, Qt, QEvent, Signal, QAbstractTableModel, QAbstractItemModel, QModelIndex
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QSplitter,
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QFormLayout,
    QLineEdit,
    QFileDialog,
    QPushButton,
    QHBoxLayout,
    QGroupBox,
    QLayout,
    QProgressBar,
    QListView,
    QTableView,
    QHeaderView,
    QAbstractItemView,
    QGridLayout
)
from PySide6 import QtWidgets, QtGui

import fssnap

def get_default_style():
    keys = QtWidgets.QStyleFactory.keys()
    assert(len(keys) > 0)
    style = QtWidgets.QStyleFactory.create(keys[0])
    return style

def get_file_icon(style):
    return style.standardIcon(QtWidgets.QStyle.SP_FileIcon)

def get_dir_icon(style):
    return style.standardIcon(QtWidgets.QStyle.SP_DirIcon)

class DefaultWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super(DefaultWidget, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        layout.addStretch()
        label = QLabel("Open a fssnap database to get started")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addStretch()
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, app, db):
        super().__init__()
        self.basedir = os.path.dirname(__file__)
        self.app = app
        self.db = db

        self.resize(1024,768)
        self.setWindowTitle("fssnap-gui")

        wdg = DefaultWidget() if not db else DatabaseWidget(db)
        self.setCentralWidget(wdg)

        db_open_action = QAction( "&Open Database", self,)
        db_open_action.setStatusTip("Open Database")
        db_open_action.triggered.connect(self.onDatabaseOpen)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(db_open_action)
        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.triggered.connect(self.app.quit)
        file_menu.addAction(quit_action)

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

    def openCentralWidget(self, widget):
        self.lastWidget = self.centralWidget()
        self.setCentralWidget(widget)

    def onCentralWidgetClosed(self):
        self.centralWidget().close()
        self.setCentralWidget(DefaultWidget())

    def onDatabaseOpen(self, s):
        ret = QFileDialog.getOpenFileName(self)
        assert(len(ret) == 2)
        dbname = ret[0]
        if len(dbname) == 0:
            return
        try:
            db = fssnap.load_db(dbname)
        except:
            ### XXX show error dialog
            print("error while loading dbname")
            return
        self.db = db
        wdg = DatabaseWidget(db)
        self.setCentralWidget(wdg)

class TreeEntry:
    def __init__(self, parent: 'TreeEntry' = None):
        self._parent = parent
        self.children = []
        self._hidden = False
        self._fetched = False
        self.name = ""
    
    def hidden(self):
        if self._hidden:
            return True
        parent = self._parent
        while parent:
            if parent._hidden:
                return True
            parent = parent.parent()
        return False        

    def parent(self):
        return self._parent
    
    def path(self):
        ret = []
        ret.append(self.name)
        parent = self._parent
        while parent:
            ret.append(parent.name)
            parent = parent.parent()
        ret.reverse()
        path = os.path.sep.join(ret[1:])
        return path
    
    def child_count(self):
        return len(self.children)
    
    def child_at_idx(self, idx: int) -> 'TreeEntry':
        assert(idx >= 0 and idx <= len(self.children))
        return self.children[idx]
    
    def child_number(self) -> int:
        if not self._parent:
            return 0
        return self._parent.children.index(self)

    def canFetchMore(self):
        return not self._fetched

    def setFetched(self):
        self._fetched = True

class FileEntry(TreeEntry):
    def __init__(self, name: str, flags: int, parent: 'TreeEntry' = None):
        super().__init__(parent)
        self.name = name
        self.flags = flags

    def canFetchMore(self):
        return False

class DirEntry(TreeEntry):
    def __init__(self, name: str, flags: int, parent: 'TreeEntry' = None):
        super().__init__(parent)
        self.name = name
        self.flags = flags

class FileTreeModel(QAbstractItemModel):
    def __init__(self, db):
        super().__init__()

        root = TreeEntry(None)
        path_root = db.common_prefix_path()
        base = path_root
        paths = db.path_children(path_root)

        if len(base) > 0 and base[-1] != "/":
            base = base + "/"

        children = []
        if len(paths) == 1:
            path = paths[0]
            p = path.path
            base = p
            if len(p) > 0 and p[-1] == "/":
                p = p[:-1]
            children = db.path_children(p)
        elif len(paths) > 1:
            children = paths

        for chld in children:
            if chld.path.endswith("/"):
                et = DirEntry(chld.path[len(base):-1], chld.flags, root)
            else:
                et = FileEntry(chld.path[len(base):], chld.flags, root)
            root.children.append(et)
        root.setFetched()

        self.root = root
        self.base_path = base
        self.db = db
        self.style = get_default_style()
        self.icon_file = get_file_icon(self.style)
        self.icon_dir = get_dir_icon(self.style)


    def columnCount(self, parent: QModelIndex = None) -> int:
        return 2

    def headerData(self, col: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if orientation != Qt.Horizontal:
            return None
        if role != Qt.DisplayRole:
            return None
        if col == 0:
            return self.base_path
        elif col == 1:
            return "perms"
        return None

    def get_entry(self, idx: QModelIndex = QModelIndex()) -> TreeEntry:
        if not idx.isValid():
            return self.root
        entry = idx.internalPointer()
        if entry:
            return entry

    def index(self, row: int, col: int, parent_idx: QModelIndex = QModelIndex()) -> QModelIndex:
        if parent_idx.isValid() and parent_idx.column() != 0:
            return QModelIndex()
        parent = self.get_entry(parent_idx)
        if not parent:
            return QModelIndex()
        child = parent.child_at_idx(row)
        if not child:
            return QModelIndex()
        return self.createIndex(row, col, child)

    def parent(self, idx: QModelIndex = QModelIndex()) -> QModelIndex:
        if not idx.isValid():
            return QModelIndex()
        child = self.get_entry(idx)
        if not child:
            return QModelIndex()
        parent = child.parent()
        if parent == self.root or parent is None:
            return QModelIndex()
        return self.createIndex(parent.child_number(), 0, parent)

    def data(self, idx: QModelIndex, role: int=None):
        if not idx.isValid():
            return None

        col = idx.column()
        entry = self.get_entry(idx)

        if role == Qt.DisplayRole:
            if col == 1:
                if self.db.is_annotated():
                    return fssnap.flags_to_string(entry.flags)
                else:
                    return "--- ---"
            elif col == 0:
                return entry.name
            return None
        elif role == Qt.DecorationRole:
            if col == 0:
                if isinstance(entry, FileEntry):
                    return self.icon_file
                elif isinstance(entry, DirEntry):
                    return self.icon_dir
            return None
        elif role == Qt.ToolTipRole:
            return entry.path()
        elif role == Qt.BackgroundRole:
            return None
        elif role == Qt.ForegroundRole:
            return None
        elif role == Qt.FontRole:
            return None
        elif role == Qt.TextAlignmentRole:
            return None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid() and parent.column() > 0:
            return 0
        entry = self.get_entry(parent)
        return entry.child_count() if entry else 0

    def fetchMore(self, parent):
        te = self.get_entry(parent)
        path = os.path.join(self.base_path, te.path())
        base = path
        off = len(base)
        if len(path) > 0 and path[-1] == "/":
            path = path[:-1]
        else:
            off += 1

        children = self.db.path_children(path)
        self.beginInsertRows(parent, 0, len(children))
        for chld in children:
            if chld.path.endswith("/"):
                et = DirEntry(chld.path[off:-1], chld.flags, te)
            else:
                et = FileEntry(chld.path[off:], chld.flags, te)
            te.children.append(et)
        self.endInsertRows()
        te.setFetched()

    def canFetchMore(self, parent):
        te = self.get_entry(parent)
        if te.canFetchMore():
            return True
        return False

    def adjustRoot(self):
        base = []
        parent = self.root
        while len(parent.children) == 1:
            base.append(parent.name)
            parent = parent.children[0]
        self.root = parent
        self.base_path = f"{os.path.sep}".join(base)

class FileTreeWidget(QWidget):
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            raise ValueError("missing database variable")

        self.db, *args = args
        super(FileTreeWidget, self).__init__(*args, **kwargs)

        self.gridLayout = QGridLayout(self)
        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.treeView = QtWidgets.QTreeView(self.frame)
        self.le = QtWidgets.QLineEdit(self.frame)
        self.le.returnPressed.connect(self.searchclick)
        self.pathcount = QtWidgets.QLabel(f"Total Path Count: {self.db.path_count()}")
        self.pathcount.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.pathlabel = QtWidgets.QLabel("")
        self.pathlabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.gridLayout_2.addWidget(self.le, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.treeView, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.pathcount, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.pathlabel, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        treemodel = FileTreeModel(self.db)
        self.treeView.setModel(treemodel)
        self.treeView.header().resizeSection(0, 300)
        self.treeView.clicked.connect(self.tree_clicked)
        self.treeView.doubleClicked.connect(self.tree_dblclicked)

    def tree_clicked(self, idx):
        model = self.treeView.model()
        te = model.get_entry(idx)
        selected_path = os.path.join(model.base_path, te.path())
        self.pathlabel.setText(f"Path Selected: {selected_path}")

    def tree_dblclicked(self, idx):
        model = self.treeView.model()
        te = model.get_entry(idx)
        if te.canFetchMore():
            model.fetchMore(idx)
    
    def searchclick(self):
        self.le.setEnabled(False)
        ftext = self.le.text()
        try:
            db = self.db.path_filter(ftext)
            treemodel = FileTreeModel(db)
            self.pathcount.setText(f"Total Path Count: {db.path_count()}")
            self.treeView.setModel(treemodel)
        except:
            pass
        self.le.setEnabled(True)

class DatabaseWidget(QWidget):
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            raise ValueError("missing database variable")
        self.db, *args = args
        super(DatabaseWidget, self).__init__(*args, **kwargs)
        layout = QHBoxLayout()
        self.fileTreeWidget = FileTreeWidget(self.db)
        layout.addWidget(self.fileTreeWidget)
        self.fileTreeWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.setLayout(layout)
	
def main():
    db = fssnap.load_db(sys.argv[1]) if len(sys.argv) >= 2 else None 

    app = QApplication(sys.argv)
    window = MainWindow(app, db)
    window.show()

    app.exec()

    sys.exit(1)

if __name__ == "__main__":
    main()
