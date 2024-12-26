from flask import Flask, render_template, request
import os
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/save_metadata', methods=['POST'])
def save_metadata():
    # Formdan gelen verileri al
    kaynak_id = request.form['kaynakID']
    kaynak_adi = request.form['kaynakAdi']
    kaynak_detay = request.form['kaynakDetay']
    kaynak_url = request.form['kaynakURL']
    kaynak_zaman = request.form['kaynakZamanDamgasi']

    # XML oluştur
    root = Element('WebKaynak')
    SubElement(root, 'KaynakID').text = kaynak_id
    SubElement(root, 'KaynakAdi').text = kaynak_adi
    SubElement(root, 'KaynakDetay').text = kaynak_detay
    SubElement(root, 'KaynakURL').text = kaynak_url
    SubElement(root, 'KaynakZamanDamgasi').text = kaynak_zaman

    xml_str = xml.dom.minidom.parseString(tostring(root)).toprettyxml(indent="  ")

    # Raporu kaydet
    if not os.path.exists('reports'):
        os.mkdir('reports')

    file_path = os.path.join('reports', f'{kaynak_id}.xml')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)

    return f"XML dosyası başarıyla kaydedildi: {file_path}"

if __name__ == '__main__':
    app.run(debug=True)