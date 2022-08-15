import argparse
import sys
from TableGeneration.GenerateTable import GenerateTable


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num', type=int, default=1, help='the number of generate table')
    # output path
    parser.add_argument('--output', type=str, default='output/simple_table')  # data save path
    # courp path
    parser.add_argument('--ch_dict_path', type=str, default='dict/ch_news.txt')
    parser.add_argument('--en_dict_path', type=str, default='dict/en_corpus.txt')

    # table settings

    # cell box type
    parser.add_argument('--cell_box_type', type=str, default='cell',
                        help='cell: use cell location as cell box; text: use location of text in cell as cell box')
    # row and col
    parser.add_argument('--min_row', type=int, default=3, help='min rows in table')
    parser.add_argument('--max_row', type=int, default=15, help='max rows in table')
    parser.add_argument('--min_col', type=int, default=3, help='min cols in table')
    parser.add_argument('--max_col', type=int, default=10, help='max cols in table')
    # row and col span
    parser.add_argument('--max_span_row_count', type=int, default=3, help='max span rows')
    parser.add_argument('--max_span_col_count', type=int, default=3, help='max span cols')
    parser.add_argument('--max_span_value', type=int, default=10, help='max value in rowspan and colspan')
    # txts lens
    parser.add_argument('--min_txt_len', type=int, default=2, help='min number of char in cell')
    parser.add_argument('--max_txt_len', type=int, default=10, help='max number of char in cell')
    # color
    parser.add_argument('--color_prob', type=float, default=0, help='the prob of color cell')
    # cell size
    parser.add_argument('--cell_max_width', type=int, default=0, help='max width of cell')
    parser.add_argument('--cell_max_height', type=int, default=0, help='max height of cell')
    # windows size
    parser.add_argument('--brower_width', type=int, default=1920, help='width of brower')
    parser.add_argument('--brower_height', type=int, default=2440, help='height of brower')
    parser.add_argument('--brower', type=str, default='chrome', help='chrome or firefox')

    args = parser.parse_args()
    if args.brower == 'chrome' and sys.platform == 'darwin':
        print('firefox is recommend for Mac OS, bug you choice is chrome')
        sys.exit(0)
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    t = GenerateTable(output=args.output,
                      ch_dict_path=args.ch_dict_path,
                      en_dict_path=args.en_dict_path,
                      cell_box_type=args.cell_box_type,
                      min_row=args.min_row,
                      max_row=args.max_row,
                      min_col=args.min_col,
                      max_col=args.max_col,
                      min_txt_len=args.min_txt_len,
                      max_txt_len=args.max_txt_len,
                      max_span_row_count=args.max_span_row_count,
                      max_span_col_count=args.max_span_col_count,
                      max_span_value=args.max_span_value,
                      color_prob=args.color_prob,
                      cell_max_width=args.cell_max_width,
                      cell_max_height=args.cell_max_height,
                      brower=args.brower,
                      brower_width=args.brower_width,
                      brower_height=args.brower_height)

    t.gen_table_img(args.num)
    t.close()
