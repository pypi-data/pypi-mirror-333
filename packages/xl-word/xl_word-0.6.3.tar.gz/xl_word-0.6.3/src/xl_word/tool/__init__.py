from xl_word.tool.gui import *
from xl_word.tool.utility import SuperWordFile
import os


class WordTemplateEditor:
    """Word模板编辑器"""

    def __init__(self):
        """初始化编辑器"""
        self.app = App({
            'title': 'XiLong DOCX Toolkit',
            'size': (420, 330),
            'loc': (500, 300)
        })
        self.root = self.app.instance
        self._init_ui()

    def _init_ui(self):
        """初始化UI界面"""
        self.main_frame = Frame(self.root, relief='ridge', borderwidth=1)
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # 创建notebook
        self.notebook = self.app.notebook(self.main_frame)
        self.notebook.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # 创建DOCX选项卡
        self.docx_frame = Frame(self.notebook)
        self.notebook.add(self.docx_frame, text='DOCX')
        
        # 创建XML选项卡
        self.xml_frame = Frame(self.notebook)
        self.notebook.add(self.xml_frame, text='XML')
        
        self._create_docx_tab()
        self._create_xml_tab()

    def _create_docx_tab(self):
        """创建DOCX选项卡内容"""
        # 创建拖拽区域
        self.docx_drop_label = Label(self.docx_frame, text="拖拽DOCX文件到这里", relief="solid")
        self.docx_drop_label.pack()
        self.docx_drop_label.place(x=30, y=30, width=350, height=40)
        
        # 绑定拖拽事件
        self.docx_drop_label.drop_target_register("DND_Files")
        self.docx_drop_label.dnd_bind('<<Drop>>', self._on_docx_drop)

        # 提取按钮组
        extract_buttons = [
            ('提取document', self._extract_document, 30),
            ('提取header', self._extract_header, 155),
            ('提取footer', self._extract_footer, 280)
        ]
        
        for text, command, x in extract_buttons:
            btn = self.app.button(
                self.docx_frame, text, command, width=13
            )
            btn.pack()
            btn.place(x=x, y=90)

        # 反编译按钮组
        decompile_buttons = [
            ('反编译document', self._decompile_document, 30),
            ('反编译header', self._decompile_header, 155),
            ('反编译footer', self._decompile_footer, 280)
        ]
        
        for text, command, x in decompile_buttons:
            btn = self.app.button(
                self.docx_frame, text, command, width=13
            )
            btn.pack()
            btn.place(x=x, y=120)

        # DOCX转XML按钮
        convert_buttons = [
            ('DOCX转XML(竖向)', self._word2xml_v, 30, 180),
            ('DOCX转XML(横向)', self._word2xml_h, 220, 180)
        ]

        for text, command, x, y in convert_buttons:
            btn = self.app.button(
                self.docx_frame, text, command, width=20
            )
            btn.pack()
            btn.place(x=x, y=y)

    def _create_xml_tab(self):
        """创建XML选项卡内容"""
        # 创建拖拽区域
        self.xml_drop_label = Label(self.xml_frame, text="拖拽XML文件到这里", relief="solid")
        self.xml_drop_label.pack()
        self.xml_drop_label.place(x=30, y=30, width=350, height=40)
        
        # 绑定拖拽事件
        self.xml_drop_label.drop_target_register("DND_Files")
        self.xml_drop_label.dnd_bind('<<Drop>>', self._on_xml_drop)

        # 编译按钮组
        compile_buttons = [
            ('反编译', self._decompile_xml, 30, 90),
            ('编译', self._compile_xml, 220, 90)
        ]

        for text, command, x, y in compile_buttons:
            btn = self.app.button(
                self.xml_frame, text, command, width=20
            )
            btn.pack()
            btn.place(x=x, y=y)

        # XML转DOCX按钮
        convert_buttons = [
            ('XML转DOCX(竖向)', self._xml2word_v, 30, 150),
            ('XML转DOCX(横向)', self._xml2word_h, 220, 150)
        ]

        for text, command, x, y in convert_buttons:
            btn = self.app.button(
                self.xml_frame, text, command, width=20
            )
            btn.pack()
            btn.place(x=x, y=y)

    def _on_docx_drop(self, event):
        """处理DOCX文件拖拽"""
        file_path = event.data
        # 移除可能存在的花括号
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        if file_path.endswith('.docx'):
            self.current_file = file_path
            self.docx_drop_label.config(text=f"当前文件: {os.path.basename(file_path)}")
        else:
            self.app.alert("错误", "请拖拽DOCX文件(.docx)")

    def _on_xml_drop(self, event):
        """处理XML文件拖拽"""
        file_path = event.data
        # 移除可能存在的花括号
        if file_path.startswith('{') and file_path.endswith('}'):
            file_path = file_path[1:-1]
        
        if file_path.endswith('.xml'):
            self.current_xml_file = file_path
            self.xml_drop_label.config(text=f"当前文件: {os.path.basename(file_path)}")
        else:
            self.app.alert("错误", "请拖拽XML文件(.xml)")

    # DOCX文件操作方法
    def _get_edit_input(self):
        """获取编辑输入"""
        if not hasattr(self, 'current_file'):
            self.app.alert("错误", "请先拖拽DOCX文件")
            return None, None
            
        folder = os.path.dirname(self.current_file)
        file = os.path.basename(self.current_file)
        return folder, file

    def _extract_document(self):
        """提取document.xml"""
        folder, file = self._get_edit_input()
        if folder and file:
            SuperWordFile(folder, file).extract('document.xml')

    def _extract_header(self):
        """提取header.xml"""
        folder, file = self._get_edit_input()
        if folder and file:
            SuperWordFile(folder, file).extract('header.xml')

    def _extract_footer(self):
        """提取footer.xml"""
        folder, file = self._get_edit_input()
        if folder and file:
            SuperWordFile(folder, file).extract('footer.xml')

    def _decompile_document(self):
        """反编译document.xml"""
        folder, file = self._get_edit_input()
        if folder and file:
            SuperWordFile(folder, file).extract('document.xml', decompile=True)

    def _decompile_header(self):
        """反编译header.xml"""
        folder, file = self._get_edit_input()
        if folder and file:
            SuperWordFile(folder, file).extract('header.xml', decompile=True)

    def _decompile_footer(self):
        """反编译footer.xml"""
        folder, file = self._get_edit_input()
        if folder and file:
            SuperWordFile(folder, file).extract('footer.xml', decompile=True)

    def _word2xml_h(self):
        """DOCX转XML(横向)"""
        SuperWordFile.word2xml('h')

    def _word2xml_v(self):
        """DOCX转XML(竖向)"""
        SuperWordFile.word2xml('v')

    def _xml2word_h(self):
        """XML转DOCX(横向)"""
        SuperWordFile.xml2word('h')

    def _xml2word_v(self):
        """XML转DOCX(竖向)"""
        SuperWordFile.xml2word('v')

    def _compile_xml(self):
        """编译XML文件"""
        if not hasattr(self, 'current_xml_file'):
            self.app.alert("错误", "请先拖拽XML文件")
            return

        try:
            # 读取XML文件
            with open(self.current_xml_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()

            # 编译处理
            from xl_word.compiler import XMLCompiler
            compiler = XMLCompiler()
            processed_content = compiler.compile_template(xml_content)

            # 保存处理后的文件
            output_path = os.path.join(
                os.path.dirname(self.current_xml_file),
                f'{SuperWordFile.timestamp()}_compiled.xml'
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            os.startfile(os.path.dirname(output_path))
            # self.app.alert("成功", f"已保存编译后的文件: {os.path.basename(output_path)}")
            
        except Exception as e:
            raise e
            self.app.alert("错误", f"编译失败: {str(e)}")

    def _decompile_xml(self):
        """反编译XML文件"""
        if not hasattr(self, 'current_xml_file'):
            self.app.alert("错误", "请先拖拽XML文件")
            return

        try:
            # 读取XML文件
            with open(self.current_xml_file, 'r', encoding='utf-8') as f:
                xml_content = f.read()

            # 反编译处理
            from xl_word.compiler import XMLCompiler
            compiler = XMLCompiler()
            processed_content = compiler.decompile_template(xml_content)

            # 保存处理后的文件
            output_path = os.path.join(
                os.path.dirname(self.current_xml_file),
                f'{SuperWordFile.timestamp()}_decompiled.xml'
            )
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_content)
            
            os.startfile(os.path.dirname(output_path))
            # self.app.alert("成功", f"已保存反编译后的文件: {os.path.basename(output_path)}")
            
        except Exception as e:
            raise e
            self.app.alert("错误", f"反编译失败: {str(e)}")

    def run(self):
        """运行编辑器"""
        self.app.run()


if __name__ == '__main__':
    editor = WordTemplateEditor()
    editor.run()