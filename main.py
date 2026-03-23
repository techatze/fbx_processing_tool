from pathlib import Path
from fbx_functions import *
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QListWidget, QVBoxLayout, QHBoxLayout, QWidget, QMainWindow, QPushButton, \
    QTextEdit, QProgressBar, QFileDialog, QLabel, QComboBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Fbx File Processor')


        #Layouts
        main_layout = QVBoxLayout()
        second_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        #Widgets
        self.fbx_list = QListWidget()

        self.log_text = QTextEdit(readOnly=True)

        self.choose_process = QComboBox()
        self.choose_process.addItems(['', 'Analyze FBX','Find Meshes','Export Single Mesh',
                                      'Export All/Rename','Axis Swap'])
        self.choose_process.currentTextChanged.connect(self.on_process_changed)


        self.choose_application = QComboBox()
        self.choose_application.addItems(['None','Maya (Y-Up)','OpenGL (Z-Up)','DirectX'])
        self.choose_application.hide()


        self.confirm_button = QPushButton('Confirm')
        self.confirm_button.clicked.connect(self.execute_selected_process)

        self.output_path_button = QPushButton("Set Output Path")
        self.output_path_button.clicked.connect(self.output_folder)

        self.clear_log = QPushButton('Clear log')
        self.clear_log.clicked.connect(self.delete_log)

        self.output_path_label = QLabel()


        #menu
        file_open = QAction('&Open',self)
        file_open.setStatusTip('Open new file')
        file_open.triggered.connect(self.show_dialog)


        menubar = self.menuBar()
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(file_open)

        #Formatting layouts
        second_layout.addWidget(self.fbx_list)

        button_layout.addWidget(self.choose_process)
        button_layout.addWidget(self.choose_application)
        button_layout.addWidget(self.confirm_button)

        button_layout.addWidget(self.output_path_button)
        second_layout.addLayout(button_layout)
        second_layout.addWidget(self.output_path_label)
        second_layout.addWidget(self.log_text)
        second_layout.addWidget(self.clear_log)


        main_layout.addLayout(second_layout)


        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


    def show_dialog(self):
        """Opens file browser and adds all .fbx files of a folder in QListWidget(self.fbx_list)."""
        self.fbx_list.clear()
        self.fbx_path = QFileDialog.getExistingDirectory(self, 'Open File')
        self.assets_to_import = list(Path(self.fbx_path).glob("*.fbx"))

        if self.fbx_path:
            for fbx in self.assets_to_import:
                self.fbx_list.addItem(fbx.stem)



    def output_folder(self):
        """Sets an 'Output Folder' from browser and shows the full path on a QLabel."""
        self.output_path = QFileDialog.getExistingDirectory(self,'Output Folder')
        self.output_path_label.setText(f'Output path: {self.output_path}')



    def validate_inputs(self):
        """Validate if Fbx files were found and output path is selected."""
        if not self.assets_to_import:
            self.log_text.append('No FBX files found.')
            return False

        if not hasattr(self, "output_path"):
            self.log_text.append("No output folder selected")
            return False

        return True



    def export_single_mesh(self):
        """Exports a single mesh from each fbx file of the QListWidget."""
        if not self.validate_inputs():
            return

        for fbx_file in self.assets_to_import:
            try:
                manager,scene = load_fbx(str(fbx_file))
                self.log_text.append(f'[OK] Loaded: {fbx_file.name}')

                mesh_nodes = get_mesh_nodes(scene)

                if not mesh_nodes:
                    self.log_text.append(f"{fbx_file.name}: No meshes found.")
                    continue

                mesh = mesh_nodes[0]
                output_file = f"{self.output_path}/{mesh.GetName()}.fbx"
                export_single_mesh(manager,mesh,output_file)

                self.log_text.append(f"[OK] Exported: {mesh.GetName()}.fbx")

                manager.Destroy()

            except Exception as e:
                self.log_text.append(f"[ERROR] {fbx_file.name}: {str(e)}")



    def analyze_fbx(self):
        """Scene Inspection for each fbx file of the QListWidget."""
        if not self.assets_to_import:
            self.log_text.append('No FBX files found.')
            return

        for fbx_file in self.assets_to_import:
            try:
                manager,scene = load_fbx(str(fbx_file))
                self.log_text.append(f'\n[FILE] {fbx_file.name}')

                lines = traverse_scene(scene)

                for line in lines:
                    self.log_text.append(line)

                manager.Destroy()
            except Exception as e:
                self.log_text.append(f"[ERROR] {fbx_file.name}: {str(e)}")



    def find_meshes(self):
        """Finds all the eMeshes from each fbx file of the QListWidget."""
        if not self.assets_to_import:
            self.log_text.append("No FBX files found")
            return

        for fbx_file in self.assets_to_import:
            try:
                manager,scene = load_fbx(str(fbx_file))

                self.log_text.append(f"\n[FILE] {fbx_file.name}")

                mesh_nodes = get_mesh_nodes(scene)

                self.log_text.append(f"Found {len(mesh_nodes)} meshes:")

                for node in mesh_nodes:
                    self.log_text.append(f" - {node.GetName()}")

                manager.Destroy()

            except Exception as e:
                self.log_text.append(f"[ERROR] {fbx_file.name}: {str(e)}")



    def export_all_rename(self):
        """Export all meshes from all fbx files in the QListWidget and rename them."""
        if not self.validate_inputs():
            return

        for fbx_file in self.assets_to_import:
            try:
                manager,scene = load_fbx(str(fbx_file))

                mesh_nodes = get_mesh_nodes(scene)

                if not mesh_nodes:
                    self.log_text.append(f"{fbx_file.name}: No meshes found")
                    continue

                self.log_text.append(f"\n[FILE] {fbx_file.name}")

                for i,mesh in enumerate(mesh_nodes):
                    output_name = make_output_name(str(fbx_file),mesh,i)
                    output_path = os.path.join(self.output_path,output_name)

                    export_single_mesh(manager,mesh,output_path)

                    self.log_text.append(f'[OK] Exported: {output_name}')

                manager.Destroy()

            except Exception as e:
                self.log_text.append(f"[ERROR] {fbx_file.name}: {str(e)}")



    def delete_log(self):
        """Delete log button."""
        self.log_text.clear()



    def on_process_changed(self,process):
        """Show/Hide Axis Selection Options"""
        if process == 'Axis Swap':
            self.choose_application.show()
        else:
            self.choose_application.hide()



    def get_selected_axis(self):
        """Get the selected Axis option from the self.choose_application list."""
        return self.choose_application.currentText()



    def axis_swap_process(self):
        """Change of Axis for each fbx file of the QListWidget."""
        if not self.validate_inputs():
            return

        axis_option = self.get_selected_axis()

        for fbx_file in self.assets_to_import:
            try:
                manager,scene = load_fbx(str(fbx_file))

                convert_axis(scene,axis_option)

                mesh_nodes = get_mesh_nodes(scene)

                for i,mesh in enumerate(mesh_nodes):
                    output_name = make_output_name(str(fbx_file), mesh, i)
                    output_path = os.path.join(self.output_path,output_name)

                    export_single_mesh(manager,mesh,output_path)

                    self.log_text.append(f"[OK] Exported: {output_name} - Changed to {self.choose_application.currentText()}")

                manager.Destroy()

            except Exception as e:
                self.log_text.append(f"[ERROR] {fbx_file.name}: {str(e)}")



    def execute_selected_process(self):
        """Selection of which process to execute."""
        process = self.choose_process.currentText()

        if process == 'Export Single Mesh':
            self.export_single_mesh()
        elif process == 'Analyze FBX':
            self.analyze_fbx()
        elif process == 'Find Meshes':
            self.find_meshes()
        elif process == 'Export All/Rename':
            self.export_all_rename()
        elif process == 'Axis Swap':
            self.axis_swap_process()



app = QApplication([])
window = MainWindow()
window.show()
app.exec()