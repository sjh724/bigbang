from flask import Flask, request, render_template
from wtforms import Form, StringField, validators

from bigbang import MysqlBruter, FtpBruter, SshBruter

app = Flask(__name__)


class LoginForm(Form):
    host = StringField("host", [validators.data_required()])
    type = StringField("type", [validators.data_required()])


@app.route("/", methods=['GET', 'POST'])
def login():
    myForm = LoginForm(request.form)
    print(request.method)
    if request.method == 'POST':
        message = "Success"
        if myForm.host.data and myForm.type.data and myForm.validate():
            host = myForm.host.data
            type = myForm.type.data
            ufile = "username.txt"
            pfile = "password.txt"
            if host:
                if type == 'mysql':
                    mysql = MysqlBruter(host, ufile, pfile)
                    results = mysql.run()
                    username = results[0].get("username")
                    password = results[0].get("password")
                elif type == 'ssh':
                    mysql = SshBruter(host, ufile, pfile)
                    results = mysql.run()
                    username = results[0].get("username")
                    password = results[0].get("password")
                elif type == 'ftp':
                    mysql = FtpBruter(host, ufile, pfile)
                    results = mysql.run()
                    username = results[0].get("username")
                    password = results[0].get("password")
            else:
                message = "参数错误"
                render_template("index.html", message=message, form=myForm)
            return render_template("sucess.html", username=username, password=password)
        else:
            print("type must be ssh or ftp or mysql")
        return render_template("index.html", message=message, form=myForm)
    else:
        message = "Failed Login"
        return render_template('index.html', message=message, form=myForm)


if __name__ == '__main__':
    app.run(debug=True)
