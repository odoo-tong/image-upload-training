import base64

from odoo_csv_tools.lib import mapper
from odoo_csv_tools.lib.transform import Processor


def my_field_mapper(line):
    field = line['extra']
    files = field.split(',')
    map = []
    for file in files:
        if not file:
            continue
        path = '/home/odoo/Desktop/odoo/partner/image-upload/image/' + file

        with open(path, "rb") as image_file:
            map.append(base64.b64encode(image_file.read()).decode('utf-8'))
            image_file.close()
    return map

def main():
    processor = Processor('data/product.template.raw.csv', delimiter=',', conf_file="config/localhost.conf")
    product_mapping = {
        'id': mapper.val('id'),
        'image_1920': mapper.binary('image_1920', '/home/odoo/Desktop/odoo/partner/image-upload/image/'),
    }
    processor.process(product_mapping, 'exports/product.template.csv', {})
    image_mapping = {
        'id': mapper.m2m_id_list('import_product_image', 'extra'),
        'name': mapper.m2m_value_list('extra'),
        'image_1920': my_field_mapper,
        'product_tmpl_id/id': mapper.val('id'),
    }
    processor.process(image_mapping, 'exports/product.image.csv', {}, m2m=True)
    processor.write_to_file("exports/product_template.sh", python_exe='', path='')

if __name__ == "__main__":
    main()
