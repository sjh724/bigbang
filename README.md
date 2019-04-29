##环境要求，
    python3.6
    mysql

##操作步骤
0、修改配置文件config.py中的数据库配置信息
1、pip install -r request.txt ----  安装好所需要的环境<br>
2、创建了名为“test_one”的数据库<br>
        ps：前提是你已经安装好了mysql<br>
3、在项目路径：python manage.py shell进入shell环境<br>
        接着：db.create_all()创建所有的表<br>
4、退出shell在根目录运行：python manage.py runserver就可以在本地看到项目啦<br>

