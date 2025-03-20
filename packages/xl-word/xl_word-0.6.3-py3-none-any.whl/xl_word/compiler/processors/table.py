from xl_word.compiler.processors.base import BaseProcessor
import re


class TableProcessor(BaseProcessor):
    """处理表格相关的XML标签"""
    @classmethod
    def compile(cls, xml: str) -> str:
        xml = cls._process_xl_table(xml)
        xml = cls._process_xl_th(xml)
        xml = cls._process_xl_tr(xml)
        xml = cls._process_xl_tc(xml)
        return xml
        
    @classmethod
    def _process_xl_table(cls, xml: str) -> str:
        def process_table(match):
            style_str, content = match.groups()
            content = content.strip()
            styles = {}
            if style_str:
                styles = dict(pair.split(':') for pair in style_str.split(';') if pair.strip())
            tbl_props = []
            if 'align' in styles:
                tbl_props.append(f'<w:jc w:val="{styles["align"]}"/>')
            if styles.get('border') == 'none':
                tbl_props.append('''<w:tblBorders>
                <w:top w:color="auto" w:space="0" w:sz="0" w:val="none"/>
                <w:left w:color="auto" w:space="0" w:sz="0" w:val="none"/>
                <w:bottom w:color="auto" w:space="0" w:sz="0" w:val="none"/>
                <w:right w:color="auto" w:space="0" w:sz="0" w:val="none"/>
                <w:insideH w:color="auto" w:space="0" w:sz="0" w:val="none"/>
                <w:insideV w:color="auto" w:space="0" w:sz="0" w:val="none"/>
            </w:tblBorders>''')
            else:
                tbl_props.append('''<w:tblBorders>
                    <w:top w:color="auto" w:space="0" w:sz="4" w:val="single"/>
                    <w:left w:color="auto" w:space="0" w:sz="4" w:val="single"/>
                    <w:bottom w:color="auto" w:space="0" w:sz="4" w:val="single"/>
                    <w:right w:color="auto" w:space="0" w:sz="4" w:val="single"/>
                    <w:insideH w:color="auto" w:space="0" w:sz="4" w:val="single"/>
                    <w:insideV w:color="auto" w:space="0" w:sz="4" w:val="single"/>
                </w:tblBorders>''')
            
            tbl_props.extend([
                '<w:tblW w:type="auto" w:w="0"/>',
                '<w:tblInd w:type="dxa" w:w="0"/>',
                '''<w:tblCellMar>
                    <w:top w:type="dxa" w:w="0"/>
                    <w:left w:type="dxa" w:w="0"/>
                    <w:bottom w:type="dxa" w:w="0"/>
                    <w:right w:type="dxa" w:w="0"/>
                </w:tblCellMar>'''
            ])
            
            return f'''<w:tbl>
                    <w:tblPr>
                        {chr(10).join(tbl_props)}
                    </w:tblPr>{content}</w:tbl>'''
            
        return cls._process_tag(xml, r'<xl-table(?:[^>]*?style="([^"]*)")?[^>]*>(.*?)</xl-table>', process_table)
    @classmethod
    def _process_xl_th(cls, xml: str) -> str:
        def process_th(match):
            content = match.group(1)
            # Add font-weight:bold to all xl-p tags inside xl-tc
            def add_bold_style(tc_match):
                tc_attrs, tc_content = tc_match.groups()
                
                def add_bold_to_p(p_match):
                    full_tag = p_match.group(0)
                    if 'style="' in full_tag:
                        haha = re.sub(r'style="([^"]*)"', 
                                    lambda m: f'style="{m.group(1)};font-weight:bold"' if 'font-weight' not in m.group(1) else m.group(0), 
                                    full_tag)
                        return haha
                    else:
                        return full_tag.replace('<xl-p', '<xl-p style="font-weight:bold"')
                
                tc_content = re.sub(r'<xl-p[^>]*>.*?</xl-p>', add_bold_to_p, tc_content, flags=re.DOTALL)
                return f'<xl-tc {tc_attrs}>{tc_content}</xl-tc>'
            
            content = re.sub(r'<xl-tc\s+([^>]+)>(.*?)</xl-tc>', add_bold_style, content, flags=re.DOTALL)
            return f'<xl-tr header="1">{content}</xl-tr>'
            
        return cls._process_tag(xml, r'<xl-th>(.*?)</xl-th>', process_th)
    
    @classmethod
    def _process_xl_tr(cls, xml: str) -> str:
        def process_tr(match):
            attrs, content = match.groups()
            tr_props_str= ''
            tr_props_str+= '<w:tblHeader/>' if 'header' in attrs else ''
            tr_props_str+= '<w:cantSplit/>' if 'cant-split' in attrs else ''
            
            height_match = re.search(r'height="(\d+)"', attrs)
            if height_match:
                height = height_match.group(1)
                tr_props_str+= f'<w:trHeight w:val="{height}"/>'
            
            other_attrs = re.findall(r'(\w+)="([^"]*)"', attrs)
            filtered_attrs = [(k,v) for k,v in other_attrs if k not in ['header', 'cant-split']]
            attrs_str = ' '.join([f'{k}="{v}"' for k,v in filtered_attrs])
            tr_props_str = f'<w:trPr>{tr_props_str}</w:trPr>'
            
            return f'<w:tr{" " + attrs_str if attrs_str else ""}>{tr_props_str}{content}</w:tr>'
            
        return cls._process_tag(xml, r'<xl-tr([^>]*)>(.*?)</xl-tr>', process_tr)

    @classmethod
    def _process_xl_tc(cls, xml: str) -> str:
        def process_tc(match):
            attrs, content = match.groups()
            attrs_dict = cls._extract_attrs(attrs, ['width', 'span', 'align', 'merge'])

            if not re.search(r'<[^>]+>', content):
                content = f'<xl-p>{content}</xl-p>'

            tc_props_str = ''
            width, span, align, merge = cls.retrieve(attrs_dict, ['width', 'span', 'align', 'merge'])
            tc_props_str += (f'<w:tcW w:type="dxa" w:w="{width}"/>') if width else ''
            tc_props_str += (f'<w:gridSpan w:val="{span}"/>') if span else ''
            tc_props_str += (f'<w:vAlign w:val="{align}"/>') if align else ''
            tc_props_str += '<w:vMerge w:val="restart"/>' if merge == 'start' else ('<w:vMerge/>' if merge else '')
            return f'<w:tc>\n                    <w:tcPr>{tc_props_str}</w:tcPr>{content}</w:tc>'
        data  = cls._process_tag(xml, r'<xl-tc([^>]*)>(.*?)</xl-tc>', process_tc)
        return data
    
    @classmethod
    def decompile(cls, xml: str) -> str:
        """将w:tbl标签转换为xl-table标签"""
        xml = cls.decompile_tbl(xml)
        xml = cls.decompile_tr(xml)
        return xml

    @classmethod
    def decompile_tbl(cls, xml: str) -> str:
        def process_word_table(match):
            full_tbl = match.group(0)
            
            styles = {}
            
            align_match = re.search(r'<w:jc\s+w:val="([^"]+)"/>', full_tbl)
            if align_match:
                styles['align'] = align_match.group(1)
            
            border_match = re.search(r'<w:tblBorders>(.*?)</w:tblBorders>', full_tbl, re.DOTALL)
            if border_match:
                border_content = border_match.group(1)
                if re.search(r'w:val="none"', border_content) and not re.search(r'w:val="single"', border_content):
                    styles['border'] = 'none'
            
            content_match = re.search(r'<w:tbl>.*?<w:tblPr>.*?</w:tblPr>(.*?)</w:tbl>', full_tbl, re.DOTALL)
            content = content_match.group(1) if content_match else ""
            
            style_str = ';'.join([f"{k}:{v}" for k, v in styles.items()]) if styles else ""
            
            return f'<xl-table style="{style_str}">{content}</xl-table>'
        
        return cls._process_tag(xml, r'<w:tbl>.*?</w:tbl>', process_word_table)

    @classmethod
    def decompile_tr(cls, xml: str) -> str:
        def process_word_tr(match):
            full_tr = match.group(0)
            content = match.group(1)
            attrs = {}

            tr_pr_match = re.search(r'<w:trPr>(.*?)</w:trPr>', full_tr, flags=re.DOTALL)
            tr_pr_str = tr_pr_match.group(1) if tr_pr_match else ''

            if '<w:tblHeader/>' in tr_pr_str:
                attrs['header'] = '1'
            
            if '<w:cantSplit/>' in tr_pr_str:
                attrs['cant-split'] = '1'
            
            height_match = re.search(r'<w:trHeight\s+w:val="([^"]+)"/>', tr_pr_str)
            if height_match:
                attrs['height'] = height_match.group(1)

            align_match = re.search(r'<w:jc\s+w:val="([^"]+)"/>', tr_pr_str)
            if align_match:
                attrs['align'] = align_match.group(1)
            attrs_str = ' '.join([f'{k}="{v}"' for k, v in attrs.items()]) if attrs else ""
            attrs_str = f' {attrs_str}' if attrs_str else ""

            def process_word_tc(match):
                full_tc = match.group(0)
                attrs = {}
                
                width_match = re.search(r'<w:tcW.*w:w="([^"]+)".*/>', full_tc)
                if width_match:
                    attrs['width'] = width_match.group(1)
                
                span_match = re.search(r'<w:gridSpan\s+w:val="([^"]+)"/>', full_tc)
                if span_match:
                    attrs['span'] = span_match.group(1)
                
                align_match = re.search(r'<w:vAlign\s+w:val="([^"]+)"/>', full_tc)
                if align_match:
                    attrs['align'] = align_match.group(1)
                
                vmerge_match = re.search(r'<w:vMerge(?:\s+w:val="([^"]+)")?/>', full_tc)
                if vmerge_match:
                    val = vmerge_match.group(1)
                    if val == "restart":
                        attrs['merge'] = 'start'
                    else:
                        attrs['merge'] = 'continue'
                
                content_match = re.search(r'<w:tc>.*?<w:tcPr>.*?</w:tcPr>(.*?)</w:tc>', full_tc, re.DOTALL)
                content = content_match.group(1) if content_match else ""
                
                attrs_str = ' '.join([f'{k}="{v}"' for k, v in attrs.items()]) if attrs else ""
                
                return f'<xl-tc {attrs_str}>{content}</xl-tc>'
        
            matches = list(re.finditer(r'<w:tc>.*?</w:tc>', content, re.DOTALL))
            content = ''
            for match in matches:
                full_tc = match.group(0)
                full_tc = cls._process_tag(full_tc, r'<w:tc>.*?</w:tc>', process_word_tc)
                content += full_tc
            
            if 'header' in attrs:
                return f'<xl-th{attrs_str}>{content}</xl-th>'
            else:
                return f'<xl-tr{attrs_str}>{content}</xl-tr>'
        
        return cls._process_tag(xml, r'<w:tr[^>]*>(.*?)</w:tr>', process_word_tr)
