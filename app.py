from flask import Flask, render_template, request, send_file
import base64
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate():
    fn = request.form['fn']
    n = request.form['n']
    nickname = request.form['nickname']
    email = request.form['email']
    tel = request.form['tel']
    bday = request.form['bday']
    address = request.form['address']
    label = request.form['label']
    tz = request.form['tz']
    geo = request.form['geo']
    title = request.form['title']
    role = request.form['role']
    logo = request.form['logo']
    agent = request.form['agent']
    org = request.form['org']
    categories = request.form['categories']
    note = request.form['note']
    url = request.form['url']
    instagram = request.form['x_socialprofile_instagram']
    telegram = request.form['x_socialprofile_telegram']
    
    photo = request.files['photo']
    photo_base64 = base64.b64encode(photo.read()).decode('utf-8')
    
    vcf_content = f"""
BEGIN:VCARD
VERSION:3.0
FN;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{fn}
N;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{n}
NICKNAME;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{nickname}
EMAIL;CHARSET=UTF-8;type=HOME:{email}
PHOTO;ENCODING=BASE64;jpeg:{photo_base64}
TEL;TYPE=HOME,VOICE:{tel}
BDAY;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{bday}
ADR;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:;;;{address}
LABEL;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{label}
TZ;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{tz}
GEO;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{geo}
TITLE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{title}
ROLE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{role}
LOGO;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{logo}
AGENT;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{agent}
ORG;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{org}
CATEGORIES;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{categories}
NOTE;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{note}
URL;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:{url}
X-SOCIALPROFILE;TYPE=Instagram:{instagram}
X-SOCIALPROFILE;TYPE=Telegram:{telegram}
END:VCARD
    """.strip()
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download VCF</title>
</head>
<body>
    <script>
        window.onload = function() {{
            const vcfContent = `{vcf_content.replace('\\n', '\\\\n')}`;
            const blob = new Blob([vcfContent], {{ type: 'text/vcard' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'test.vcf';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }};
    </script>
</body>
</html>
    """
    
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.html'
    filepath = os.path.join('output', filename)
    
    os.makedirs('output', exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
