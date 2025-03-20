"""
   Copyright 2015 University of Auckland

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import os.path

from PySide6 import QtCore, QtGui, QtWidgets

from cmapps.neon.core.definitions import DEFAULT_VIEW_NAME
from cmapps.neon.view.dialogs.aboutdialog import AboutDialog
from cmapps.neon.view.ui_mainwindow import Ui_MainWindow
from cmapps.neon.undoredo.commands import CommandEmpty

from cmlibs.widgets.addviewwidget import AddView
from cmlibs.widgets.editabletabbar import EditableTabBar
from cmlibs.widgets.fieldlisteditorwidget import FieldListEditorWidget
from cmlibs.widgets.logviewerwidget import LogViewerWidget
from cmlibs.widgets.materialeditorwidget import MaterialEditorWidget
from cmlibs.widgets.mesheditorwidget import MeshEditorWidget
from cmlibs.widgets.modelsourceseditorwidget import ModelSourcesEditorWidget, ModelSourcesModel
from cmlibs.widgets.regioneditorwidget import RegionEditorWidget
from cmlibs.widgets.sceneeditorwidget import SceneEditorWidget
from cmlibs.widgets.scenelayoutchooserdialog import SceneLayoutChooserDialog
from cmlibs.widgets.sceneviewereditorwidget import SceneviewerEditorWidget
from cmlibs.widgets.spectrumeditorwidget import SpectrumEditorWidget
from cmlibs.widgets.tessellationeditorwidget import TessellationEditorWidget
from cmlibs.widgets.timeeditorwidget import TimeEditorWidget
from cmlibs.widgets.viewwidget import ViewWidget

OTHER_WINDOWS = ["Log Viewer"]
BOTTOM_DOCK_AREA = ["Time Editor", "Log Viewer"]


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, model):
        super(MainWindow, self).__init__()
        self._model = model

        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.viewTabWidget.setTabBar(EditableTabBar(self.parentWidget()))

        self._location = None  # The last location/directory used by the application
        self._current_view = None

        self._undoRedoStack = QtGui.QUndoStack(self)

        # Pre-create dialogs
        self._editors = {}
        self._primary_dock_widget = None
        self._primary_bottom_dock_widget = None

        self._setup_editors()
        self._register_editors()

        self._view_action_group = QtGui.QActionGroup(self)
        self._view_actions = []
        self._setup_views()

        self._add_dock_widgets()

        self._make_connections()

        # Set the undo redo stack state
        self._undoRedoStack.push(CommandEmpty())
        self._undoRedoStack.clear()

        self._update_ui()

        self._read_settings()

        self._on_document_changed()

    def _make_connections(self):
        self._ui.action_Quit.triggered.connect(self.close)
        self._ui.action_New.triggered.connect(self._new_triggered)
        self._ui.action_Open.triggered.connect(self._open_triggered)
        self._ui.action_About.triggered.connect(self._about_triggered)
        self._ui.action_Save.triggered.connect(self._save_triggered)
        self._ui.action_Save_As.triggered.connect(self._save_as_triggered)
        self._ui.action_Snapshot.triggered.connect(self._snapshot_triggered)
        self._ui.action_Preferences.triggered.connect(self._preferences_triggered)
        self._ui.action_Clear.triggered.connect(self._clear_triggered)
        self._ui.viewTabWidget.tabCloseRequested.connect(self._view_tab_close_requested)
        self._ui.viewTabWidget.currentChanged.connect(self._current_view_changed)
        tab_bar = self._ui.viewTabWidget.tabBar()
        tab_bar.tabTextEdited.connect(self._view_tab_text_edited)

        self._undoRedoStack.indexChanged.connect(self._undo_redo_stack_index_changed)
        self._undoRedoStack.canUndoChanged.connect(self._ui.action_Undo.setEnabled)
        self._undoRedoStack.canRedoChanged.connect(self._ui.action_Redo.setEnabled)

        self._model.documentChanged.connect(self._on_document_changed)

    def _update_ui(self):
        modified = self._model.isModified()
        self._ui.action_Save.setEnabled(modified)
        recents = self._model.getRecents()
        self._ui.action_Clear.setEnabled(len(recents))

    def _add_dock_widgets(self):
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self._primary_dock_widget)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, self._primary_bottom_dock_widget)
        primary_doc_widgets = [self._primary_dock_widget.windowTitle(), self._primary_bottom_dock_widget.windowTitle()]
        for editor_name in self._editors:
            if editor_name not in primary_doc_widgets:
                if editor_name in BOTTOM_DOCK_AREA:
                    self.tabifyDockWidget(self._primary_bottom_dock_widget, self._editors[editor_name].parentWidget())
                else:
                    self.tabifyDockWidget(self._primary_dock_widget, self._editors[editor_name].parentWidget())

    def _setup_editor(self, editor, hidden=True):
        title = editor.windowTitle()
        self._editors[title] = editor

        dock_widget = QtWidgets.QDockWidget(title, self)
        dock_widget.setObjectName(f"dockWidget{title.replace(' ', '')}")
        editor.setObjectName(f"dockWidgetContents{title.replace(' ', '')}")
        dock_widget.setWidget(editor)
        dock_widget.setHidden(hidden)

    def _setup_editors(self):
        widget = ModelSourcesEditorWidget()
        self._setup_editor(widget, False)
        self._primary_dock_widget = widget.parentWidget()

        self._setup_editor(RegionEditorWidget())
        self._setup_editor(MaterialEditorWidget())
        self._setup_editor(MeshEditorWidget())
        self._setup_editor(SceneEditorWidget())

        widget = SceneviewerEditorWidget(self)
        self._setup_editor(widget)
        widget.parentWidget().visibilityChanged.connect(widget.setEnableUpdates)

        self._setup_editor(SpectrumEditorWidget(self))
        self._setup_editor(TessellationEditorWidget())
        self._setup_editor(TimeEditorWidget())
        self._setup_editor(FieldListEditorWidget())

        widget = LogViewerWidget(self)
        self._setup_editor(widget)
        self._primary_bottom_dock_widget = widget.parentWidget()

    def _register_editors(self):
        for editor_name in self._editors:
            if editor_name not in OTHER_WINDOWS:
                self._register_editor(self._editors[editor_name].parentWidget())

        self._ui.menu_View.addSeparator()

        for editor_name in self._editors:
            if editor_name in OTHER_WINDOWS:
                self._register_other_editor(self._editors[editor_name].parentWidget())

    def _register_editor(self, editor):
        menu = self._ui.menu_View

        toggle_action = editor.toggleViewAction()
        toggle_action.triggered.connect(self._view_dock_widget)
        menu.addAction(toggle_action)

    def _add_view_clicked(self):
        dlg = SceneLayoutChooserDialog(self)
        dlg.setModal(True)
        if dlg.exec_():
            layout = dlg.selected_layout()
            document = self._model.getDocument()
            view_manager = document.getViewManager()
            view_manager.addViewByType(layout, DEFAULT_VIEW_NAME)
            view_manager.setActiveView(layout)
            self._views_changed(view_manager)

    def _view_dock_widget(self, show):
        """
        If we are showing the dock widget we will make it current i.e. make sure it is visible if tabbed.
        """
        if show:
            sender_text = self.sender().text()
            for tab_bar in self.findChildren(QtWidgets.QTabBar):
                for index in range(tab_bar.count()):
                    tab_text = tab_bar.tabText(index)
                    if tab_text == sender_text:
                        tab_bar.setCurrentIndex(index)
                        return

    def _get_editor_action(self, action_name):
        action = None
        actions = self._ui.menu_View.actions()
        existing_actions = [a for a in actions if a.text() == action_name]
        if existing_actions:
            action = existing_actions[0]

        return action

    # def _createDialogs(self):
    #     self._snapshot_dialog = SnapshotDialog(self, self._ui.one_gl_widget_to_rule_them_all)
    #     self._snapshot_dialog.setZincContext(self._model.getZincContext())

    #     self._preferences_dialog = PreferencesDialog(self)

    def _write_settings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        settings.setValue('location', self._location)
        settings.setValue('geometry', self.saveGeometry())

        settings.beginWriteArray('recents')
        recents = self._model.getRecents()
        for i, r in enumerate(recents):
            settings.setArrayIndex(i)
            settings.setValue('item', r)
        settings.endArray()
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        # settings.setValue('state', self._snapshot_dialog.serialize())
        settings.endGroup()

    def _read_settings(self):
        settings = QtCore.QSettings()
        settings.beginGroup('MainWindow')
        geometry = settings.value('geometry')
        if geometry is not None:
            self.restoreGeometry(geometry)
        self._location = settings.value('location', QtCore.QDir.homePath())

        size = settings.beginReadArray('recents')
        for i in range(size):
            settings.setArrayIndex(i)
            self._add_recent(settings.value('item'))
        settings.endArray()
        settings.endGroup()

        settings.beginGroup('SnapshotDialog')
        # self._snapshot_dialog.deserialize(settings.value('state', ''))
        settings.endGroup()

        self._update_ui()

    def _add_recent(self, recent):
        actions = self._ui.menu_Open_Recent.actions()
        insert_before_action = actions[0]
        self._model.addRecent(recent)
        recent_action = QtGui.QAction(self._ui.menu_Open_Recent)
        recent_action.setText(recent)
        self._ui.menu_Open_Recent.insertAction(insert_before_action, recent_action)
        recent_action.triggered.connect(self._open)

    def _set_current_view(self, index):
        v = self._ui.viewTabWidget.widget(int(index))
        self._change_view(v)
        self._post_change_view()

    def _store_current_view(self):
        pass

    def _pre_change_view(self):
        pass

    def _change_view(self, view):
        self._ui.viewTabWidget.setCurrentWidget(view)

    def _post_change_view(self):
        pass

    def _register_other_editor(self, editor):
        action = self._get_editor_action("Other Windows")
        if action is None:
            menu = self._ui.menu_View.addMenu("Other Windows")
            menu.setEnabled(True)
        else:
            menu = action.menu()

        toggle_action = editor.toggleViewAction()
        toggle_action.triggered.connect(self._view_dock_widget)
        menu.addAction(toggle_action)

    def _view_tab_close_requested(self, index):
        document = self._model.getDocument()
        view_manager = document.getViewManager()
        view_manager.removeView(index)
        self._views_changed(view_manager)

    def _view_tab_text_edited(self, index, value):
        document = self._model.getDocument()
        view_manager = document.getViewManager()
        view = view_manager.getView(index)
        view.setName(value)

    def _current_view_changed(self, index):
        document = self._model.getDocument()
        view_manager = document.getViewManager()
        view_manager.setActiveView(self._ui.viewTabWidget.tabText(index))
        self._current_sceneviewer_changed()

    def _setup_views(self):
        icon = QtGui.QIcon(":/widgets/images/icons/list-add-icon.png")
        btn = QtWidgets.QToolButton()
        btn.setStyleSheet("border-radius: 0.75em; border-width: 1px; border-style: solid; border-color: dark-grey;"
                          " background-color: grey; min-width: 1.5em; min-height: 1.5em; margin-right: 1em;")
        btn.setIcon(icon)
        btn.setAutoFillBackground(True)
        btn.clicked.connect(self._add_view_clicked)

        self._ui.viewTabWidget.setCornerWidget(btn)

    def _current_sceneviewer_changed(self):
        current_widget = self._ui.viewTabWidget.currentWidget()
        if current_widget:
            sceneviewer = current_widget.getActiveSceneviewer()
            sceneviewer_widget = current_widget.getActiveSceneviewerWidget()
            self._editors["Sceneviewer Editor"].setSceneviewer(sceneviewer)
            self._editors["Mesh Editor"].setSceneviewerWidget(sceneviewer_widget)

    def _views_changed(self, view_manager):
        views = view_manager.getViews()
        active_view = view_manager.getActiveView()

        # Remove existing views from menu
        for view_action in self._view_actions:
            self._view_action_group.removeAction(view_action)
            self._ui.menu_View.removeAction(view_action)

        self._view_actions = []

        # Remove all views.
        self._ui.viewTabWidget.clear()
        tab_bar = self._ui.viewTabWidget.tabBar()

        if views:
            tab_bar.set_editable(True)
            active_widget = None
            separator_action = self._ui.menu_View.addSeparator()
            separator_action.setActionGroup(self._view_action_group)
            self._view_actions.append(separator_action)
            # Instate views.
            for v in views:
                w = ViewWidget(v.getScenes(), v.getGridSpecification(), self._ui.viewTabWidget)
                # w.graphicsReady.connect(self._view_graphics_ready)
                w.currentChanged.connect(self._current_sceneviewer_changed)
                w.setContext(view_manager.getZincContext())
                view_name = v.getName()
                self._ui.viewTabWidget.addTab(w, view_name)

                if active_view == view_name:
                    active_widget = w

                action_view = QtGui.QAction(view_name, self)
                action_view.setData(w)
                # action_view.setCheckable(True)
                action_view.setActionGroup(self._view_action_group)
                action_view.triggered.connect(self._view_triggered)
                action_view.setCheckable(True)
                self._ui.menu_View.addAction(action_view)
                self._view_actions.append(action_view)

            if active_widget is not None:
                self._ui.viewTabWidget.setCurrentWidget(w)
            else:
                self._ui.viewTabWidget.setCurrentIndex(0)
            self._ui.viewTabWidget.setTabsClosable(True)
        else:
            tab_bar.set_editable(False)

            add_view = AddView()
            add_view.clicked.connect(self._add_view_clicked)
            self._ui.viewTabWidget.addTab(add_view, "Add View")
            self._ui.viewTabWidget.setTabsClosable(False)

    def _view_triggered(self):
        v = self.sender().data()
        self._pre_change_view()
        self._change_view(v)
        self._post_change_view()

    def _on_document_changed(self):
        document = self._model.getDocument()
        self._model.setCurrentUndoRedoIndex(1)
        rootRegion = document.getRootRegion()
        zincRootRegion = rootRegion.getZincRegion()

        # need to pass new Zinc context to dialogs and widgets using global modules
        zincContext = document.getZincContext()
        self._editors["Spectrum Editor"].setSpectrums(document.getSpectrums())
        self._editors["Material Editor"].setMaterials(document.getMaterials())
        self._editors["Tessellation Editor"].setTessellations(document.getTessellations())
        self._editors["Time Editor"].setZincContext(zincContext)
        # self._snapshot_dialog.setZincContext(zincContext)

        model_sources_model = ModelSourcesModel(document, [])
        self._editors["Model Sources Editor"].setModelSourcesModel(zincRootRegion, model_sources_model)

        # need to pass new root region to the following
        self._editors["Region Editor"].setRootRegion(rootRegion)
        self._editors["Scene Editor"].setZincRootRegion(zincRootRegion)
        self._editors["Sceneviewer Editor"].setZincRootRegion(zincRootRegion)
        self._editors["Field List Editor"].setRootArgonRegion(rootRegion)
        self._editors["Field List Editor"].setTimekeeper(zincContext.getTimekeepermodule().getDefaultTimekeeper())

        view_manager = document.getViewManager()
        self._views_changed(view_manager)

    def _visualisation_view_ready(self):
        self._visualisation_view_ready = True
        if self._visualisation_view_state_update_pending:
            print('applying pending restore:')
            self._restore_sceneviewer_state()

    def _save_triggered(self):
        if self._model.getLocation() is None:
            self._save_as_triggered()
        else:
            self._record_sceneviewer_state()
            self._model.save()

    def _save_as_triggered(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption='Choose file ...', dir=self._location, filter="Neon Files (*.neon *.json);;All (*.*)")
        if filename:
            self._location = os.path.dirname(filename)
            self._model.setLocation(filename)
            self._record_sceneviewer_state()
            self._model.save()

    def _restore_sceneviewer_state(self):
        print('restore sceneveiwer state:')
        document = self._model.getDocument()
        sceneviewer_state = document.getSceneviewer().serialize()
        # self._visualisation_view.setSceneviewerState(sceneviewer_state)
        # self.dockWidgetContentsSceneviewerEditor.setSceneviewer(self._visualisation_view.getSceneviewer())
        self._visualisation_view_state_update_pending = False

    def _record_sceneviewer_state(self):
        document = self._model.getDocument()
        view_manager = document.getViewManager()
        for index in range(self._ui.viewTabWidget.count()):
            tab = self._ui.viewTabWidget.widget(index)
            tab_layout = tab.layout()

            view = view_manager.getView(index)
            view.setName(self._ui.viewTabWidget.tabText(index))

            rows = tab_layout.rowCount()
            columns = tab_layout.columnCount()
            for r in range(rows):
                for c in range(columns):
                    sceneviewer_widget = tab_layout.itemAtPosition(r, c).widget()
                    view.updateSceneviewer(r, c, sceneviewer_widget.get_zinc_sceneviewer())

    def _undo_redo_stack_index_changed(self, index):
        self._model.setCurrentUndoRedoIndex(index)

    def _about_triggered(self):
        d = AboutDialog(self)
        d.exec_()

    def _snapshot_dialog_ready(self):
        document = self._model.getDocument()
        rootRegion = document.getRootRegion()
        zincRootRegion = rootRegion.getZincRegion()
        scene = zincRootRegion.getScene()
        self._snapshot_dialog.setScene(scene)

    def _snapshot_triggered(self):
        if self._snapshot_dialog.getLocation() is None and self._location is not None:
            self._snapshot_dialog.setLocation(self._location)

        if self._snapshot_dialog.exec_():
            if self._location is None:
                self._location = self._snapshot_dialog.getLocation()
            filename = self._snapshot_dialog.getFilename()
            wysiwyg = self._snapshot_dialog.getWYSIWYG()
            width = self._snapshot_dialog.getWidth()
            height = self._snapshot_dialog.getHeight()
            self._visualisation_view.saveImage(filename, wysiwyg, width, height)

    def _preferences_triggered(self):
        if self._preferences_dialog.exec_():
            pass  # Save the state

    def _new_triggered(self):
        self._model.new()

    def _open_model(self, filename):
        success = self._model.load(filename)
        if success:
            self._location = os.path.dirname(filename)
            self._add_recent(filename)
        else:
            QtWidgets.QMessageBox.warning(self, "Load failure", "Failed to load file " + filename + ". Refer to logger window for more details", QtWidgets.QMessageBox.StandardButton.Ok)
            self._model.new()  # in case document half constructed; emits documentChanged

        self._update_ui()

    def _open_triggered(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Choose file ...', dir=self._location, filter="Neon Files (*.neon *.json);;All (*.*)")

        if filename:
            self._open_model(filename)

    def _open(self):
        """
        Open a model from a recent file.
        """
        filename = self.sender().text()
        self._ui.menu_Open_Recent.removeAction(self.sender())
        self._model.removeRecent(filename)
        self._open_model(filename)

    def _clear_triggered(self):
        self._model.clearRecents()
        actions = self._ui.menu_Open_Recent.actions()
        for action in actions[:-2]:
            self._ui.menu_Open_Recent.removeAction(action)

        self._update_ui()

    def _confirm_close(self):
        # Check to see if the Workflow is in a saved state.
        if self._model.isModified():
            ret = QtWidgets.QMessageBox.warning(self, 'Unsaved Changes', 'You have unsaved changes, would you like to save these changes now?',
                                                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if ret == QtWidgets.QMessageBox.StandardButton.Yes:
                self._save_triggered()

    def _quit_application(self):
        self._confirm_close()
        self._write_settings()

    def closeEvent(self, event):
        self._quit_application()
        super(MainWindow, self).closeEvent(event)
