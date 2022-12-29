import csv

class Vacancy:
    def __init__(self, a):
        self.area_name = a['area_name']
        self.year = int(a['published_at'][:4])
        self.name = a['name']
        self.salary_currency = a['salary_currency']
        self.salary_to = int(float(a['salary_to']))
        self.salary_from = int(float(a['salary_from']))
        self.salary_average = self.convert_currency[self.salary_currency] * (self.salary_from + self.salary_to) / 2
    convert_currency = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

class DataSet:
    def __init__(self, name, vac):
        self.file_name = name
        self.vacancy_name = vac

    def read(self):
        kolvo = 0
        salaries_dict = {}
        headers_list = []
        vac_num = {}
        vac_num_name = {}
        # city_sal = {}
        city_sal = {}
        num_sal = {}
        salary_vac_name = {}

        with open(self.file_name, mode='r', encoding='utf-8-sig') as f:
            read = csv.reader(f)
            counter=0
            for i, j in enumerate(read):
                if i == 0:
                    headers_list = j
                    lenght = len(j)
                elif '' not in j and len(j) == lenght:
                    vac = Vacancy(dict(zip(headers_list, j)))
                    if vac.area_name not in num_sal:
                        num_sal[vac.area_name] = 1
                    else:
                        counter += 1
                        num_sal[vac.area_name] += 1
                    if vac.area_name not in city_sal:
                        city_sal[vac.area_name] = [vac.salary_average]
                    else:
                        counter += 1
                        city_sal[vac.area_name].append(vac.salary_average)
                    if vac.name.find(self.vacancy_name) != -1:
                        if vac.year not in salary_vac_name:
                            salary_vac_name[vac.year] = [vac.salary_average]
                        else:
                            counter+=1
                            salary_vac_name[vac.year].append(vac.salary_average)
                        if vac.year not in vac_num_name:
                            vac_num_name[vac.year] = 1
                        else:
                            vac_num_name[vac.year] += 1
                    if vac.year not in vac_num:
                        vac_num[vac.year] = 1
                    else:
                        vac_num[vac.year] += 1
                    kolvo += 1
                    if vac.year not in salaries_dict:
                        salaries_dict[vac.year] = [vac.salary_average]
                    else:
                        salaries_dict[vac.year].append(vac.salary_average)

        if not salary_vac_name:
            vac_num_name = vac_num.copy()
            vac_num_name = dict([(key, 0) for key, value in vac_num_name.items()])
            salary_vac_name = salaries_dict.copy()
            salary_vac_name = dict([(key, []) for key, value in salary_vac_name.items()])
        vac_statistics2 = {}
        for year, list_of_salaries in salary_vac_name.items():
            if len(list_of_salaries) != 0:
                vac_statistics2[year] = int(sum(list_of_salaries) / len(list_of_salaries))
            else:
                vac_statistics2[year] = 0
        vac_statistics1 = {}
        for year, list_of_salaries in salaries_dict.items():
            vac_statistics1[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        print('Динамика уровня зарплат по годам: ' + str(vac_statistics1))
        vac_statistic3 = {}
        for year, list_of_salaries in city_sal.items():
            # vac_statistic3[year] = int(sum(list_of_salaries)
            # print(len(vac_statistic3))
            vac_statistic3[year] = int(sum(list_of_salaries) / len(list_of_salaries))
        print('Динамика количества вакансий по годам: ' + str(vac_num))
        print('Динамика уровня зарплат по годам для выбранной профессии: ' + str(vac_statistics2))
        vac_statistic4 = {}
        for year, list_of_salaries in num_sal.items():
            vac_statistic4[year] = round(list_of_salaries / kolvo, 4)
        print('Динамика количества вакансий по годам для выбранной профессии: ' + str(vac_num_name))
        vac_statistic4 = list(filter(lambda a: a[-1] >= 0.01, [(key, value) for key, value in vac_statistic4.items()]))
        vac_statistic4.sort(key=lambda a: a[-1], reverse=True)
        stats5 = vac_statistic4.copy()
        vac_stats6 = []
        vac_statistic4 = dict(vac_statistic4)
        vac_stats6 = list(vac_statistic4)
        vac_statistic3 = list(filter(lambda a: a[0] in list(vac_statistic4.keys()), [(key, value) for key, value in vac_statistic3.items()]))
        vac_statistic3.sort(key=lambda a: a[-1], reverse=True)
        vac_stats6.append(vac_statistic4)
        vac_statistic3 = dict(vac_statistic3[:10])
        print('Уровень зарплат по городам (в порядке убывания): ' + str(vac_statistic3))
        print('Доля вакансий по городам (в порядке убывания): ' + str(dict(stats5[:10])))

class InputConnect:
    def __init__(self):
        self.file_name = input('Введите название файла: ')
        self.vacancy_name = input('Введите название профессии: ')

        all_data = DataSet(self.file_name, self.vacancy_name)
        all_data.read()

if __name__ == '__main__':
    InputConnect()