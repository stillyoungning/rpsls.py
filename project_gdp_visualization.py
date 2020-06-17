# coding:gbk
"""
�ۺ���Ŀ:������ʷ���ݻ������༰����ӻ�
���ߣ�������
���ڣ�2020/6/10
Ŀ�꣺ͨ����дpython���򣬶�ȡ���������ļ����ڴ˻����ϸ���Ҫ������ݽ�������ͷ��࣬����ϵ��������ʵ���Զ�����������������GDP�����Ե�ͼ��ʽ���ӻ���
"""

import csv
import math
import pygal
import pygal_maps_world


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    �������:
      filename:csv�ļ���
      keyfield:����
      separator:�ָ���
      quote:���÷�
    ���:
      ��ȡcsv�ļ����ݣ�����Ƕ���ֵ��ʽ����������ֵ�ļ���Ӧ����keyfiled���ڲ��ֵ��Ӧÿ���ڸ�������Ӧ�ľ���ֵ
    """
    result = {}
    with open(filename, newline="")as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            result[rowid] = row

    return result


pygal_countries = pygal.maps.world.COUNTRIES


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """

    �������:
    plot_countries: ��ͼ����Ҵ������ݣ��ֵ��ʽ�����м�Ϊ��ͼ����Ҵ��룬ֵΪ��Ӧ�ľ������
    gdp_countries:���и������ݣ�Ƕ���ֵ��ʽ�������ⲿ�ֵ�ļ�Ϊ���й��Ҵ��룬ֵΪ�ù��������ļ��е������ݣ��ֵ��ʽ)������Դ���ϸ�����

    �����
    ����Ԫ���ʽ������һ���ֵ��һ�����ϡ������ֵ�����Ϊ��������GDP���ݵĻ�ͼ�������Ϣ����Ϊ��ͼ������Ҵ��룬ֵΪ��Ӧ�ľ������),
    ��������Ϊ��������GDP���ݵĻ�ͼ����Ҵ���
    """
    ingdp = {}
    notingdp = set()

    kk = list(plot_countries.keys())
    vv = list(plot_countries.values())
    for i in range(len(vv)):
        if vv[i] in gdp_countries:
            ingdp[kk[i]] = vv[i]
        else:
            notingdp.add(kk[i])

    return (ingdp, notingdp)



def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    �������:
    gdpinfo:
	plot_countries: ��ͼ����Ҵ������ݣ��ֵ��ʽ�����м�Ϊ��ͼ����Ҵ��룬ֵΪ��Ӧ�ľ������
	year: �������ֵ

    �����
    �������һ���ֵ�Ͷ������ϵ�Ԫ�����ݡ������ֵ�����Ϊ��ͼ������Ҵ��뼰��Ӧ����ĳ�������GDP��ֵ����Ϊ��ͼ���и����Ҵ��룬ֵΪ�ھ�����ݣ���year����ȷ��������Ӧ������GDP����ֵ��Ϊ
    ������ʾ���㣬GDP�����ת��Ϊ��10Ϊ�����Ķ�����ʽ����GDPԭʼֵΪ2500����ӦΪlog2500��ps:����math.log()���)
    2������һ��Ϊ������GDP��������ȫû�м�¼�Ļ�ͼ����Ҵ��룬��һ������Ϊֻ��û��ĳ�ض��꣨��year����ȷ��������GDP���ݵĻ�ͼ����Ҵ���
   """
    datas = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"], gdpinfo["separator"],
                                     gdpinfo["quote"])
    dd = reconcile_countries_by_name(plot_countries, datas)
    # ��Ԫ���е��ֵ�ͼ������ݷֱ���ȡ����
    dd0 = dd[0]
    dd1 = dd[1]
    allgdp = {}
    ss1 = set()
    ss2 = set()
    kk = list(dd0.keys())
    vv = list(dd0.values())
    min = gdpinfo["min_year"]
    max = gdpinfo["max_year"]


    for i in range(len(kk)):
        ii = 0
        for j in range(min,max+1):
            if datas[vv[i]][str(j)]:
                ii=ii+1

        if datas[vv[i]][year]:
            allgdp[kk[i]] = math.log10(float(datas[vv[i]][year]))
            ss2.add(kk[i])

        if ii:
            ss2.add(kk[i])
        else:
            ss1.add(kk[i])
    ss3 = ss1 | dd1
    return (allgdp, ss3, ss2)




def render_world_map(gdpinfo, plot_countries, year, map_file):  # ������ĳ�����������GDP����(����ȱ��GDP�����Լ�ֻ���ڸ���ȱ��GDP���ݵĹ���)�Ե�ͼ��ʽ���ӻ�
    """
    Inputs:

      gdpinfo:gdp��Ϣ�ֵ�
      plot_countires:��ͼ����Ҵ������ݣ��ֵ��ʽ�����м�Ϊ��ͼ����Ҵ��룬ֵΪ��Ӧ�ľ������
      year:����������ݣ����ַ�����ʽ������"1970"
      map_file:�����ͼƬ�ļ���

    Ŀ�꣺��ָ��ĳ����������GDP�����������ͼ����ʾ������������Ϊ����ĵ�ͼƬ�ļ�
    ��ʾ�����������ӻ���Ҫ����pygal.maps.world.World()����

    """
    rr = build_map_dict_by_name(gdpinfo, plot_countries, year)
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.add(year, rr[0])
    worldmap_chart.add("missing from word bank", list(rr[1]))
    worldmap_chart.add('no data in this year', list(rr[2]))
    worldmap_chart.title = '�������GDP�ֲ�ͼ'
    worldmap_chart.render_to_file(map_file)




def test_render_world_map(year):  # ���Ժ���
    """
    �Ը����ܺ������в���
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }  # ���������ֵ�

    pygal_countries = pygal.maps.world.COUNTRIES  # ��û�ͼ��pygal���Ҵ����ֵ�

    # ����ʱ����1970��Ϊ�����Ժ����������ԣ������н�����ṩ��svg���жԱȣ�������ݿɽ��ļ���������
    render_world_map(gdpinfo, pygal_countries, year, "isp_gdp_world_name_2010.svg")


# ������Ժ�����
print("��ӭʹ������GDP���ݿ��ӻ���ѯ")
print("----------------------")
year = input("���������ѯ�ľ������:")
test_render_world_map(year)
