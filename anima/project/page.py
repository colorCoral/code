#自定义分页
#官方推荐,页码数为奇数
class PageNation:
    def __init__(self, base_url, current_page_num,total_counts,request,per_page_counts=10,page_number=5,):
        '''
        :param base_url:   分页展示信息的基础路径
        :param current_page_num:  当前页页码
        :param total_counts:  总的数据量
        :param per_page_counts:  每页展示的数据量
        :param page_number:  显示页码数
        '''

        self.base_url = base_url
        self.current_page_num = current_page_num
        self.total_counts = total_counts
        self.per_page_counts = per_page_counts
        self.page_number = page_number
        self.request = request
        try:
            self.current_page_num = int(self.current_page_num)

        except Exception:
            self.current_page_num = 1
        if self.current_page_num < 1:
            self.current_page_num = 1

        half_page_range = self.page_number // 2
        # 计算总页数
        self.page_number_count, a = divmod(self.total_counts, self.per_page_counts)


        if a:
            self.page_number_count += 1


        if self.current_page_num > self.page_number_count:
            self.current_page_num = self.page_number_count

        if self.page_number_count <= self.page_number:
            self.page_start = 1
            self.page_end = self.page_number_count
        else:
            if self.current_page_num <= half_page_range:  #2
                self.page_start = 1
                self.page_end = page_number  #5
            elif self.current_page_num + half_page_range >= self.page_number_count:
                self.page_start = self.page_number_count - self.page_number + 1
                self.page_end = self.page_number_count
            else:
                self.page_start = self.current_page_num - half_page_range
                self.page_end = self.current_page_num + half_page_range


        import copy
        from django.http.request import QueryDict

        self.params = copy.deepcopy(request.GET)

        # ?condition = qq & wd = 1 & page = 3
        # params['page'] = current_page_num
        # query_str = params.urlencode()
    #数据切片依据,起始位置
    @property
    def start_num(self):
        start_num = (self.current_page_num - 1) * self.per_page_counts
        return start_num

    #数据切片依据,终止位置
    @property
    def end_num(self):
        end_num = self.current_page_num * self.per_page_counts
        return end_num

    # 拼接HTMl标签
    def page_html(self):
        tab_html = ''
        tab_html += '<nav aria-label="Page navigation" class="pull-right"><ul class="pagination">'
        #首页
        self.params['page'] = 1
        showye = '<li><a href="{0}?{1}" aria-label="Previous" ><span aria-hidden="true">首页</span></a></li>'.format(self.base_url,self.params.urlencode())
        tab_html += showye
        # 上一页
        if self.current_page_num == 1:
            previous_page = '<li disabled><a href="#" aria-label="Previous" ><span aria-hidden="true">&laquo;</span></a></li>'
        else:
            self.params['page'] = self.current_page_num - 1
            previous_page = '<li><a href="{0}?{1}" aria-label="Previous" ><span aria-hidden="true">&laquo;</span></a></li>'.format(
                self.base_url,self.params.urlencode())
        tab_html += previous_page

        #循环生成页码标签
        for i in range(self.page_start, self.page_end + 1):
            # request.GET  {condition: qq, wd: 1,'page':1} request.GET.urlencode() condition=qq&wd=1&page=4

            self.params['page'] = i # {condition: qq, wd: 1,'page':1} urlencode() -- condition=qq&wd=1&page=4

            if self.current_page_num == i:

                one_tag = '<li class="active"><a href="{0}?{2}">{1}</a></li>'.format(self.base_url, i,self.params.urlencode()) #?condition=qq&wd=1&page=3
            else:
                one_tag = '<li><a href="{0}?{2}">{1}</a></li>'.format(self.base_url, i,self.params.urlencode())
            tab_html += one_tag

        # 下一页
        if self.current_page_num == self.page_number_count:
            next_page = '<li disabled><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
        else:
            self.params['page'] = self.current_page_num + 1
            next_page = '<li><a href="{0}?{1}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.base_url, self.params.urlencode())
        tab_html += next_page

        # 尾页
        self.params['page'] = self.page_number_count
        weiye = '<li><a href="{0}?{1}" aria-label="Previous" ><span aria-hidden="true">尾页</span></a></li>'.format(
            self.base_url, self.params.urlencode())

        tab_html += weiye
        tab_html += '</ul></nav>'

        return tab_html


#函数low鸡版
def pagenation(base_url,current_page_num,total_counts,per_page_counts=10,page_number=5):
    '''
    total_counts数据总数
    per_page_counts每页分多少条数据
    page_number = 页码显示多少个
    current_page_num 当前页
    :return:
    '''
    # all_objs_list = models.Customer.objects.all()
    # total_counts = all_objs_list.count()
    # page_number = 5

    try:
        current_page_num = int(current_page_num)

    except Exception:
        current_page_num = 1


    half_page_range = page_number//2
    #计算总页数
    page_number_count,a = divmod(total_counts,per_page_counts)
    if current_page_num < 1:
        current_page_num = 1

    if a:
        page_number_count += 1
    if current_page_num > page_number_count:
        current_page_num = page_number_count

    start_num = (current_page_num - 1) * 10
    end_num = current_page_num * 10

    if page_number_count <= page_number:
        page_start = 1
        page_end = page_number_count
    else:
        if current_page_num <= half_page_range:
            page_start = 1
            page_end = page_number
        elif current_page_num + half_page_range  >= page_number_count:
            page_start = page_number_count - page_number + 1
            page_end = page_number_count
        else:
            page_start = current_page_num - half_page_range
            page_end = current_page_num + half_page_range

    #拼接HTMl标签
    tab_html = ''
    tab_html += '<nav aria-label="Page navigation"><ul class="pagination">'

    #上一页
    if current_page_num == 1:
        previous_page = '<li disabled><a href="#" aria-label="Previous" ><span aria-hidden="true">&laquo;</span></a></li>'
    else:
        previous_page = '<li><a href="{0}?page={1}" aria-label="Previous" ><span aria-hidden="true">&laquo;</span></a></li>'.format(base_url,current_page_num-1)
    tab_html += previous_page

    for i in range(page_start,page_end+1):
        if current_page_num == i:

            one_tag = '<li class="active"><a href="{0}?page={1}">{1}</a></li>'.format(base_url,i)
        else:
            one_tag = '<li><a href="{0}?page={1}">{1}</a></li>'.format(base_url, i)
        tab_html += one_tag


    #下一页
    if current_page_num == page_number_count:
        next_page = '<li disabled><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'
    else:
        next_page = '<li><a href="{0}?page={1}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(base_url,current_page_num+1)
    tab_html+=next_page
    tab_html += '</ul></nav>'

    return tab_html,start_num,end_num
