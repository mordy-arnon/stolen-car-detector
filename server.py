from flask import *
from LicenseDetector import LicenseDetector
app = Flask(__name__)
ld = LicenseDetector()

@app.route('/')
def main():
	return render_template("index.html")

@app.route('/check', methods = ['POST'])
def success():
	if request.method == 'POST':
		f = request.files['file']
		f.save(f.filename)
		lp = ld.detect(f.filename)
		if lp=="25714701":
			return render_template("stolen.html", name=lp)
		else:
			return render_template("green.html", name=lp)

if __name__ == '__main__':
	app.run(debug=True)
