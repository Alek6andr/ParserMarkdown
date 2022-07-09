import re


class SaerchMarkDown:

    def __init__(self, markdown_fail):
        self.__markdown_fail = markdown_fail
        self.__open_a_file_and_convert_md_to_html()

    def __str__(self):
        return f"{self.saerch_headers()}{self.saerch_blokcquotes()}{self.saerch_lists()}{self.saerch_codeblocks()}" \
               f"{self.saerch_span_elements__links()}{self.saerch_emphasis()}{self.saerch_code()}{self.saerch_tabl()}"

    def __repr__(self):
        return f"{self.saerch_headers()}{self.saerch_blokcquotes()}{self.saerch_lists()}{self.saerch_codeblocks()}" \
               f"{self.saerch_span_elements__links()}{self.saerch_emphasis()}{self.saerch_code()}{self.saerch_tabl()}"

    def __open_a_file_and_convert_md_to_html(self):
        try:
            with open(f"{self.__markdown_fail}", "r", encoding="utf8") as file:
                md_text = file.read()
                md_list = md_text.split("\n")
                return md_list
        except FileNotFoundError as error:
            print(f" 'Ooops' {error= } {type(error)}")

    def __saerch(self, reg, del_symbol="\*"):
        result = []
        for f in self.__open_a_file_and_convert_md_to_html():
            # print(f)
            data = reg.findall(f)
            if data == []:
                pass
            else:
                res = re.sub(f"{del_symbol}", "", *data)
                result.append(res)
        return result

    def saerch_headers(self):
        headers = re.compile(r"^#{1,6}[^#].+#{0,6}$")
        return self.__saerch(headers, r"#")

    def saerch_blokcquotes(self):
        blokcquotes = re.compile(r"^>{1,2}.+")
        return self.__saerch(blokcquotes, r">\s{0,}")

    def saerch_lists(self):
        lis = re.compile(r"^\*{1}[^\\*].+[^\\*]$|^\+{1}.+|^\\-{1}[^\-].+[^\-]|^[1-99]{1}\..+")
        return self.__saerch(lis, r"[*\+\-\d\.]\s{0,}")

    def saerch_codeblocks(self):
        codeblocks = re.compile(r"^\s{4}[^>\s].+|^\s{8}[^>\s].+$")
        return self.__saerch(codeblocks, r"\s{4,}")

    def saerch_span_elements__links(self):
        span_elements_links = re.compile(r"^\[?.+\\]:?\s?http:\\/\\/.+\"?\'?\(?.+\)?\'?\"?")
        return self.__saerch(span_elements_links, r"^\s+\s+$")

    def saerch_emphasis(self):
        emphasis = re.compile(r"^\*{1,2}.+\*{1,2}$|^\\_{1,2}.+\\_{1,2}$")
        return self.__saerch(emphasis, r"[\*\_\+]")

    def saerch_code(self):
        code = re.compile(r"^.*`\s?.+\s?`.*")
        return self.__saerch(code, r"")

    def saerch_tabl(self):
        def data_sort(keys, datas):
            key = dict.fromkeys(keys, list())
            data = list(zip(*datas))
            tabl = []
            for i in range(len(key)):
                key[keys[i]] = data[i]
            tabl.append(key)
            return tabl

        def delete_symbol(texts):
            result = []
            for i in texts:
                i = re.sub("^\|", "", i)
                i = [re.sub("\|$", "", i).split("|")]
                result += i
            return result

        saerch_tables = re.compile(r"^(\|\s?.+\s?\|){1,99}")
        all_tabl = []
        all_key_row = []
        all_key_row_str = []
        all_row = []

        for f in self.__open_a_file_and_convert_md_to_html():
            f = saerch_tables.findall(f)
            if f != []:
                all_tabl.append(f)
        x = 0
        for index, keys in enumerate(all_tabl):
            if re.match(r"^\|-*\|{1,100}", *keys):  # поиск ключевой строки md |------|----|---|---|---|
                key_row = index
                key_row_str = all_tabl[index - 1]
                all_key_row.append(key_row)
                all_key_row_str.append(key_row_str)
            x = index

        leng_column = all_key_row[::-1]
        leng_column.insert(0, x + 2)
        leng = []
        count = 0
        for i in leng_column:
            if count:
                leng.append(count - i - 2)
            count = i
        leng_column = leng[::-1]

        index_row = []
        for i in range(len(all_key_row)):
            x = list(range(all_key_row[i] + 1, all_key_row[i] + 1 + leng_column[i]))
            index_row.append(x)

        for i in index_row:
            for j in i:
                all_row.append(all_tabl[j])
            all_row.append("-")

        x = []
        y = []
        for i in all_row:
            if i != "-":
                x += i
            else:
                y.append(x)
                x = []
        list_all_row = y

        values_dict = []
        for i in list_all_row:
            values_dict.append(delete_symbol(i))

        key_dict = []
        for i in all_key_row_str:
            key_dict.append(delete_symbol(i))
        key_dict = sum(key_dict, [])

        dicts = []
        for i in range(len(key_dict)):
            dicts += data_sort(key_dict[i], values_dict[i])
        return dicts

    # def saerch_imegas(self):
    #     imegas = re.compile(r"^!\[.+\]\((.+)\.jpg(\"?\'?.+\'?\"?)?\)")
    #     return saerch(imegas, self, r"~")


def main():
    md = SaerchMarkDown("")
    # print(md.saerch_headers())
    # print(md.saerch_blokcquotes())
    # print(md.saerch_lists())
    # print(md.saerch_codeblocks())
    # print(md.saerch_span_elements__links())
    # print(md.saerch_emphasis())
    # print(md.saerch_code())
    # print(*md.saerch_tabl(), sep="\n")


if __name__ == "__main__":
    main()
