import os
from tqdm import tqdm
import cv2
import numpy as np
import argparse


def parse_line(data_dir, line):
    import os, json
    data_line = line.decode('utf-8').strip("\n")
    info = json.loads(data_line)
    file_name = info['filename']
    cells = info['html']['cells'].copy()
    structure = info['html']['structure']['tokens'].copy()

    img_path = os.path.join(data_dir, file_name)
    if not os.path.exists(img_path):
        print(img_path)
        return None
    data = {
        'img_path': img_path,
        'cells': cells,
        'structure': structure,
        'file_name': file_name
    }
    return data


def draw_bbox(img_path, points, color=(255, 0, 0), thickness=2):
    if isinstance(img_path, str):
        img_path = cv2.imread(img_path)
    img_path = img_path.copy()
    for point in points:
        cv2.polylines(img_path, [point.astype(int)], True, color, thickness)
    return img_path


def rebuild_html(data):
    html_code = data['structure']
    cells = data['cells']
    to_insert = [i for i, tag in enumerate(html_code) if tag in ('<td>', '>')]

    for i, cell in zip(to_insert[::-1], cells[::-1]):
        if cell['tokens']:
            text = ''.join(cell['tokens'])
            # skip empty text
            sp_char_list = ['<b>', '</b>', '\u2028', ' ', '<i>', '</i>']
            text_remove_style = skip_char(text, sp_char_list)
            if len(text_remove_style) == 0:
                continue
            html_code.insert(i + 1, text)

    html_code = ''.join(html_code)
    return html_code


def skip_char(text, sp_char_list):
    """
    skip empty cell
    @param text: text in cell
    @param sp_char_list: style char and special code
    @return:
    """
    for sp_char in sp_char_list:
        text = text.replace(sp_char, '')
    return text


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str)
    parser.add_argument('--gt_path', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    label_file_path = args.gt_path

    with open(label_file_path, "rb") as f:
        data_lines = f.readlines()

    save_dir = os.path.split(label_file_path)[0] + '/show'
    os.makedirs(save_dir + '/imgs', exist_ok=True)

    f_html = open(os.path.join(save_dir, 'show.html'), 'w')
    f_html.write('<html>\n<body>\n')
    f_html.write('<table border="1">\n')
    f_html.write(
        "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
    )
    f_html.write("<tr>\n")
    f_html.write('<td>img name\n')
    f_html.write('<td>ori image</td>')
    f_html.write('<td>structure</td>')
    f_html.write('<td>box</td>')
    f_html.write("</tr>\n")

    for i, line in tqdm(enumerate(data_lines)):
        data = parse_line(args.image_dir, data_lines[i])

        if data is None:
            continue
        img = cv2.imread(data['img_path'])
        img_name = ''.join(os.path.basename(data['file_name']).split('.')[:-1])
        img_save_name = os.path.join(save_dir, 'imgs', img_name)
        cv2.imwrite(img_save_name + '.jpg', img)

        boxes = [np.array(x['bbox']) for x in data['cells']]
        show_img = draw_bbox(data['img_path'], boxes)
        cv2.imwrite(img_save_name + '_show.jpg', show_img)

        html = rebuild_html(data)

        f_html.write("<tr>\n")
        f_html.write(f'<td> imgs/{img_name}.jpg <br/>\n')
        f_html.write(f'<td><img src="imgs/{img_name}.jpg" width=640></td>')
        f_html.write('<td><table  border="1">' + html + '</table></td>')
        f_html.write(
            f'<td><img src="imgs/{img_name}_show.jpg" width=640></td>')

        f_html.write("</tr>\n")
    f_html.write('</table></body></html>')
    f_html.close()
