


def import_questionnaire():

    from openpyxl import load_workbook
    wb = load_workbook(filename = 'EMIF-AD.xlsx')
    list_sheets = wb.get_sheet_names()

    ws = wb.get_active_sheet()
    print ws
    content = []


    for ws_name in list_sheets:
        ws = wb.get_sheet_by_name(ws_name)
        for row in ws.rows:
            for c in row:
                if c.value != None:
                    print c.value

        #content.append([c.value for c in row])

    # for row in ws.iter_rows(): # it brings a new method: iter_rows()
    #
    #     row_content = []
    #     for cell in row:
    #         row_content.append(cell.internal_value)
    #         print cell.row
    #     #     # content.append(cell.internal_value)
    #     content.append(cell.row)
    #     content[cell.row].append(row_content)
    #print content


import_questionnaire()
