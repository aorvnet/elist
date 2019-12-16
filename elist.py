# This class is used to  input, statistics, and save emounts of eperimental materials
import numpy as np
import pandas as pd
class MaterialList():
    
    # 初始化类
    def __init__(self, 
                list_ori=pd.DataFrame(columns=['id', '名称', '规格', '标签', '用途', '数量', 
                                               '单位','组数', '总数', '类型', '组别', '(规格)名称'])):
        self.list_ori = list_ori
    
    
    # 美观打印表格
    def display(self, df = None):
        if df is None:
            df = self.list_ori.loc[:,['(规格)名称', '名称', '规格', '标签', '用途', '数量', '单位','组别', '组数', '类型']].copy()
        import prettytable as pt
        tb = pt.PrettyTable()
        tb.add_column('no.', df.index.to_list())
        for i in df.columns.to_list():
            tb.add_column(i, df[i].to_list())
        print(tb)
    
    
    ###  添加数据函数  ###
    def add(self, indent = '    ', input_list = [0, 1, 2, 3, 4], group_n = 1, group_type = '常规组', usedfor='', ifdisplay = False, display=display):
        # 数据初始化
        def None_f(x): return x
        keys = pd.DataFrame(['id', '名称', '规格', '标签', '用途', '数量', 
                             '单位','组数', '总数', '类型', '组别', '(规格)名称'])
        strfun_list = [None_f, None_f, None_f, None_f, None_f, float, None_f, int, float, int, None_f]
        data_default = pd.DataFrame({'id':[''], '名称':[''], '规格':[''], '标签':[''], 
                                     '用途':[usedfor], '数量':[0.0], '单位':[''], '组数':[group_n], 
                                     '总数':[0.0], '类型':[0], '组别':[group_type]}).iloc[0]
        # 输入提示内容  '请输入'
        print_prompt = ['        名称<空格>规格  :  ',
                        '        标签            :  ',
                        '        用途            :  ',
                        '        数量<空格>单位  :  ',
                        '        组数            :  ']
        # 填充序号
        column_id = [[1, 2], [3], [4], [5, 6], [7]]
        
        ##  数据输入函数  ##
        def input_fun(indent, input_i, data_old, strfun_list, data_pre):    # input_i 为 column_id 的索引，column_i 为 column_id中该索引下的元素,如:[1, 2]
            # indent: 提示语缩进, column_i: 更新列号, data_old: 待更新记录, strfun_list: 数据格式转换函数, data_pre: 前一条记录
            data_new = data_old.copy()
            input_ = input(indent + print_prompt[input_i])
            column_i = column_id[input_i]
            column_i_key = keys.iloc[column_i,0].to_list()
            if (input_ == ' '):    # 输入空格,使用前条记录值
                data_new[column_i_key] = data_pre[column_i_key].copy()
                return data_new, input_
            elif (input_ == ''):    # 直接回车,使用默认值
                data_new[column_i_key] = data_default[column_i_key].copy()
                return data_new, input_
            elif input_ in ['quit', 'back', 'reinput', 'group', 'drop', 'display']:    # 输入为特殊命令,则本次输入不更新数据
                 return data_old.copy(), input_
            else:
                value = input_.split(' ')
                try:    # 正确转换填充数据
                    for i in range(len(value)):
                        data_new[column_i_key[i]] = strfun_list[column_i[i]](value[i])
                    return data_new, input_
                except:    # 不能正确转换填充数据,提示输入不合法,本次输入不更新数据
                    print('')
                    print(indent + '输入不合法, 请重新输入...')
                    #              '        名称<空格>规格  :  '
                    return data_old.copy(), 'reinput'
        
        ##  数据更新函数  ##
        def get_data(self, indent, input_list):
            print('')
            print(indent + '请输入')
            i = 0
            try:
                data_pre_ = self.list_ori.iloc[-1].copy()
            except:
                data_pre_ = data_default.copy()
            
            data_old = data_default.copy()
            while i < len(input_list):
                data_new, input_ = input_fun(indent, input_list[i], data_old, strfun_list, data_pre = data_pre_)
                if input_ == 'quit':    # 直接退出当前记录的输入,返回'quit'提示不插入该记录数据
                    break
                elif input_ == 'back':    # 不更新数据,退回到当前记录的上一步输入  i = i - 1, 如 i < 0, 令 i = 0
                    i = max(0, i-1)
                elif input_ == 'display':    # 显示输入结果，退出循环，传递'display'放弃此次输入
                    print('')
                    display(self)
                    break
                elif input_ == 'reinput':    # 不更新数据,不更新i值,重复该记录的当前输入步骤
                    continue
                elif input_ == 'drop':    # 删除self.list_ori中的最后一条记录, 退出循环，传递'drop'放弃此次输入
                    self.list_ori = self.list_ori.iloc[:(-1),:].copy()
                    break
                elif input_ == 'group':
                    data_default[ '组别'] = input(indent + '变更组类别默认值')
                    break
                else:
                    data_new['(规格)名称'] = data_new['规格'] + data_new['名称']
                    data_new['id'] = data_new['(规格)名称'] + '(' + data_new['标签'] + ')'
                    data_old = data_new
                    i += 1
            
            return data_new, input_
        
        ###  循环录入  ###
        ifquit = ''
        while ifquit != 'quit':
            data, ifquit = get_data(self, indent, input_list)
            # 插入数据
            if ifquit not in ['quit', 'group', 'drop', 'display']:    # 如检测到 'quit', 'group', 'drop' 则不插入数据,直接跳转到下一次记录输入
                # 判断数据是否重复插入
                ifdup = False
                _unit = data['单位']
                try:
                    ifdup = ((self.list_ori['名称'] == data['名称']) 
                            & (self.list_ori['规格'] == data['规格'])
                            & (self.list_ori['标签'] == data['标签'])
                            & (self.list_ori['组别'] == data['组别'])).any()
                except:
                    pass
                try:
                    _unit = self.list_ori.loc[(self.list_ori['名称'] == data['名称']) 
                                               & (self.list_ori['规格'] == data['规格']), '单位'].iloc[0]
                except:
                    pass
                # 如果当前组的清单中已存在该物品,则要求确认,“0” 代表放弃记录,“1” 代表插入记录
                allow_add = '1'
                if ifdup:
                    print('')
                    allow_add = input(indent + '记录已存在,请输入("0" - 丢弃,"1" - 保留) :  ')
                
                if allow_add == '1':
                    if (_unit == data['单位']):
                        data['总数'] = data[ '数量'] * data[ '组数']
                        self.list_ori = self.list_ori.append(data, ignore_index = True)
                        print('')
                    else:
                        print(indent + '当前记录与已有记录的单位(' + _unit + ')不一致,请重新输入……')
                        print('')
                else:
                    print(indent + '当前记录作废')
    
    
    # 检查实验用品类型（直接材料，间接材料）
    def check(self, add=add, ifsum = False):
        if ifsum:
            self.list_ori['总数'] = self.list_ori['数量'] * self.list_ori['组数']
        # 统计中文字符数量
        def str_count(str):
            n = 0
            for s in str:
                if '\u4e00' <= s <= '\u9fff':    # 中文字符范围
                    n += 1
            return n
        
        # 核定材料类型
        self.list_ori['(规格)名称'] = self.list_ori['规格'].str.cat(self.list_ori['名称'], sep='')
        while self.list_ori['类型'].min() == 0:    # 循环检查直到所有"class"列均已不为0
            list_ori_special_name = self.list_ori['(规格)名称'] # 获取以规格名称作为标志符,去除重复后的物品列表
            
            # 修正所有"规格名称"为 list_ori_special_name[i]的记录的class值,取最大值
            for i in list_ori_special_name:
                self.list_ori.loc[self.list_ori['(规格)名称'] == i, '类型'] = self.list_ori.loc[self.list_ori['(规格)名称'] == i, '类型'].max()
            
            n_row = self.list_ori.shape[0]
            # 补充材料类型,循环检查每条记录
            for i in range(n_row):
                # class值为0时,才需要补充
                if self.list_ori.loc[i, '类型'] == 0:
                    print('')
                    _str1 = self.list_ori.loc[i,'规格'] + self.list_ori.loc[i,'名称'] + '的数量'
                    _str2 = str(self.list_ori.loc[self.list_ori['(规格)名称'] == self.list_ori.loc[i, '(规格)名称'],'总数'].sum()) + self.list_ori.loc[i, '单位']
                    _str1 = _str1.rjust(31-str_count(_str1))
                    _str2 = _str2.ljust(10-str_count(_str2))
                    print('  ' + _str1 + ' : ' + _str2 + '    ', end = '')
                    class_ = input('请输入"0"或"1"("0":间接材料,"1":直接材料):  ')
                    if class_ == '0':    # 如输入值为0,标明该special_name对应记录为间接材料,则增加原材料,并更新该special_name对应所有记录的class值为2
                        group_type_ = self.list_ori.loc[i, '(规格)名称']
                        while True:
                            try:
                                group_n_ = int(input(' '.ljust(50) + '设置组数                                 :  '))
                                break
                            except:
                                print(' '.ljust(50) + '输入不合法,请重新输入.....................')
                        
                        add(self, indent=' '.ljust(50), input_list = [0, 1, 3], group_n = group_n_, group_type = group_type_ + '准备组', usedfor = group_type_ + '准备')
                        self.list_ori.loc[self.list_ori['(规格)名称'] == self.list_ori.loc[i, '(规格)名称'], '类型'] = 2
                        break
                    if class_ == '1':    # 如输入值为1,则更新该special_name对应所有记录的class值为1
                        self.list_ori.loc[self.list_ori['(规格)名称'] == self.list_ori.loc[i, '(规格)名称'], '类型'] = 1
                        break
                    if (class_ != '0') & (class_ !='1'):
                        print(' '.ljust(50) + '只允许输入"0"或"1", 请重新输入...')
                        break
    
    
    # 实验用品数量统计数
    def stat(self):
        list_ori = self.list_ori.copy()
        list_ori['id'] = list_ori['(规格)名称'].str.cat(list_ori['单位'], sep=' ')
        list_sum = {}
        # 总数量
        list_sum_ = list_ori.loc[:,['总数', 
                                    '类型']].astype(float).groupby(list_ori['id']).agg({'总数':['sum'], 
                                                                                         '类型':['max']}).reset_index()
        list_sum_.columns = list_sum_.columns.get_level_values(0)
        list_sum = list_sum_['id'].str.split(' ', expand=True).rename(columns={0:'(规格)名称',1:'单位'})
        list_sum['总数'] = list_sum_['总数']
        list_sum['类型'] = list_sum_['类型']
        list_sum = list_sum.loc[:, ['(规格)名称', '总数', '单位', '类型']]
        # 分组数量
        list_group_ = list_ori.loc[:,['数量', '类型']].groupby( list_ori['id'].str.cat(
                                                           list_ori['组数'].astype('str'), sep= ' ').str.cat(
                                                           list_ori['组别'], sep= ' ') ).agg({'数量':['sum'], 
                                                                                                    '类型':['max']}).reset_index()
        list_group_.columns = list_group_.columns.get_level_values(0)
        list_group = list_group_['id'].str.split(' ', expand=True).rename(columns={0:'(规格)名称',1:'单位',2:'组数',3:'组别'})
        list_group['数量'] = list_group_['数量']
        list_group['总数'] = list_group['数量'] * list_group['组数'].astype(float)
        list_group['类型'] = list_group_['类型'] 
        list_group = list_group.loc[:,['组别', '(规格)名称', '数量', '组数', '总数', '单位', '类型']]
        
        list_sum = list_sum.sort_values(by = ['类型'])
        list_group = list_group.sort_values(by = ['组别', '类型'])
        self.list_sum = list_sum
        self.list_group = list_group
    
    
    # 保存统计结果到Excel文件
    def save(self):
        print('')
        # 初始化Excel文件
        filename = input('  请输入(存储路径)及文件名: ')
        nan_excel = pd.DataFrame()
        nan_excel.to_excel(filename)
        writer = pd.ExcelWriter(filename)
        # 写入Excel文件
        self.list_ori.to_excel(writer, sheet_name='清单')
        self.list_sum.to_excel(writer, sheet_name='总数量')
        self.list_group.to_excel(writer, sheet_name='分组数量')
        for sheet in self.list_group['组别'].unique():
            self.list_group.loc[self.list_group['组别'] == sheet,:].to_excel(writer, sheet_name=sheet)
        writer.save()
        writer.close()
    
    
    # 追加保存原始清单到hdf5格式文件
    def append(self):
        print('')
        filename = input('  请输入追加hdf5格式文件名（及路径）: ')
        try:
            f = pd.HDFStore(filename, 'r+')
        except:
            f = pd.HDFStore(filename, 'w')
        print('')
        _name = input('  请输入                  数据集名称: ')
        f[_name] = self.list_ori
        f.close()
    
    
    # 从hdf5格式文件载入数据到原始清单
    def load(self):
        print('')
        filename = input('  请输入　　hdf5格式文件名（及路径）: ')
        try:
            f = pd.HDFStore(filename, 'r')
            print('')
            _name = input("  请输入                  数据集名称: ")
            self.list_ori = f[_name]
            f.close()
        except:
            print('  指定的文件或数据集不存在...')
    
    
    # 编辑原始清单中数据
    # def edit(self, loc=None):
        # if loc is None:
            # try:
                # _ = self.list_ori.loc[loc[0], loc[1]]
            # except:
                # print('  输入不合法, 请重新输入...')
            # try:
                # print('  更新前数据: ')
                # display(self.list_ori.loc[[loc[0]]])
                # self.list_ori.loc[loc[0], loc[1]] = input('  请输入更正值: ')
                # print('')
                # print('  更新后数据: ')
                # display(self.list_ori.loc[[loc[0]]])
            # except:
                # print('  未知错误... ')
    
    def edit(self, logic = None, display = display):
        try:
            if (not (logic is None)):
                logic = logic.split(' ')
                _ = self.list_ori.loc[self.list_ori.loc[:, logic[0]] == logic[1], :]
                print('  更新前数据: ')
                display(self, _.iloc[:, 1:])
                def None_f(x): return x
                type_list = {'id':None_f, '名称':None_f, '规格':None_f, '标签':None_f, 
                             '用途':None_f, '数量':float, '单位':None_f, '组数':int, 
                             '总数':float, '类型':int, '组别':None_f}
                _name = input('   请输入字段名：')
                if _name != 'quit':
                    self.list_ori.loc[self.list_ori.loc[:, logic[0]] == logic[1], _name] = type_list[_name](input('   请输入更正值: '))
                    print('')
                    print('  更新后数据: ')
                    _ = self.list_ori.loc[self.list_ori.loc[:, logic[0]] == logic[1], :]
                    display(self, _.iloc[:, 1:])
        except:
            print('   未知错误...')

# jq = el.MaterialList(list_['list_ori'])
