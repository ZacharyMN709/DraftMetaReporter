import dataframe_image as dfi


def frame_to_png(frame, file_name):
    s = frame.style
    cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'td:hover',
        'props': [('background-color', '#ffffb3')]
    }
    index_names = {
        'selector': '.index_name',
        'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
    }
    headers = {
        'selector': 'th:not(.index_name)',
        'props': 'background-color: #555555; color: white;'
    }
    s.set_table_styles([cell_hover, index_names, headers])
    dfi.export(s, file_name)
    return s