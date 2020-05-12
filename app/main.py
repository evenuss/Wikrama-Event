from app import *




# LOGIN
@app.route('/', methods=['POST','GET'])
def Login():
	req = request.form
	if request.method == 'POST' and 'upload':
		print('Method : POST')
		if req['username']=='' or req['password'] == '':
			print({'status : 404',
				'message : Not Found'})
		else:
			a = mongo.db.admin.count({'username':req['username']})
			if a < 1:
				flash('Failed')
			else:
				pw = mongo.db.admin.find_one({'username':req['username']})
				b = bcrypt.check_password_hash(pw['password'], req['password'])
				if b == True:
					session['login'] = True
					session['name'] = req['username']
					print('status : 200 ok')
					return redirect(url_for('Dashboard'))
				else:
					flash('Failed')
			
	else:
		print('Method : GET')
		print('status : 200')
	return render_template('index.html')





# REGISTER OPERATOR
@app.route('/register', methods=['POST','GET'])
def Register():
	req = request.form
	if request.method=='POST':
		pw_has = bcrypt.generate_password_hash(req['password'])
		rec = mongo.db.admin.insert({
			'email':req['email'],
			'fullname':req['fullname'],
			'gender':req['gender'],
			'username':req['username'],
			'password':pw_has,
			'verified':False
		})
		flash('Success')
	else:
		pass
	return render_template('register.html')




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/newevent', methods=['POST','GET'])
def CreateEvent():
	req = request.form
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			new = mongo.db.event.insert({
				'name': req['name'],
				'foto': filename,
				'date': req['tanggal']
			})
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			

	return render_template('admin/CreateEvent_Page.html')





#SEARCH DATA
@app.route('/search',methods=['GET','POST'])
def search():
	if not request.form:
		return render_template('upload.html')
	else:
		checkRombel = mongo.db.siswa.count({'rombel':request.form['find']})
		
		if checkRombel == 0 and request.method=='POST':
			had = ['Nis','Fullname','Nickname','Rombel','Rayon','Gender']
			tbc = mongo.db.siswa.count({'rayon':request.form['find']})
			find = mongo.db.siswa.find({'rayon':request.form['find']})
		else:
			had = ['Nis','Fullname','Nickname','Rombel','Rayon','Gender']
			tbc = mongo.db.siswa.count({'rombel':request.form['find']})
			find = mongo.db.siswa.find({'rombel':request.form['find']})

	return render_template('upload.html', find=find,had=had,jml=tbc)


# UPLOAD SISWA
@app.route('/upload/siswa',methods=['GET','POST'])
def uploadSiswa():
	if 'login' in session:
		pass
	else:
		return redirect(url_for('Login'))
	tb = mongo.db.siswa.find()
	jml = mongo.db.siswa.count()
	had = ['Nis','Fullname','Nickname','Rombel','Rayon','Gender']
	if request.method=='POST':
		if not request.files['file']:
			flash('Failed')
		else:
			df = pd.read_csv(request.files['file'],delimiter=",")
			records_ = df.to_dict(orient='records')
			dict={}
			for rec in records_:
				print(rec)
				gettype = mongo.db.siswa.count({'nis':rec['nis']})
				if gettype > 0:
					print(gettype)
					print('if')
					mongo.db.siswa.update({'nis':rec['nis']},{'$set':{
							'fullname':rec['fullname'],
							'nickname':rec['nickname'],
							'rombel':rec['rombel'],
							'rayon':rec['rayon'],
							'gender':rec['gender'],
							'delete':False
						}})
				else:
					sd = mongo.db.siswa.count()
					print(sd)
					dict['_id'] = ObjectId()
					dict['nis'] = rec['nis']
					dict['fullname'] = rec['fullname']
					dict['nickname'] = rec['nickname']
					dict['rombel'] = rec['rombel']
					dict['rayon'] = rec['rayon']
					dict['gender'] = rec['gender']
					dict['delete'] = False
					print('else')
					# print(dict)
					print(rec)
					mongo.db.siswa.insert(dict)
		flash('Success!')

	return render_template('upload.html',data=tb ,had=had,jml=jml)





@app.route('/generate', methods=['GET','POST'])
def genQr():
	find = mongo.db.siswa.find()
	for rec in find:
		img_bg = Image.open('static/img/Picture1.png').crop((90,0,170,80)).resize((50,50))
		data = rec['nis']
		filename = rec['fullname']+'.png'
		img = qrcode.make(data)
		pos = ((img.size[0] - img_bg.size[0]) // 2 ,(img.size[1] - img_bg.size[1]) // 2)
		img.paste(img_bg,pos)
		img.save('./static/img/qr/'+filename)
	return 'success'




# UPLOAD NEW OPERATOR
@app.route('/upload', methods=['GET','POST'])
def uploadCSV():
	if 'login' in session:
		pass
	else:
		return redirect(url_for('Login'))
	tb = mongo.db.users.find()
	head = ['No','Nis','Name','Nickname','Rombel','Rayon','Gender']
	if 'upload' and request.method=='POST':
		if not request.files['file']:
			flash('Failed')
		else:
			df = pd.read_csv(request.files['file'],delimiter=",")
			records_ = df.to_dict(orient='records')
			dict={}
			for rec in records_:
				print(rec)
				gettype = mongo.db.users.count({'nis':rec['nis']})
				if gettype > 0:
					print(gettype)
					print('if')
					mongo.db.users.update({'nis':rec['nis']},{'$set':{
							'fullname':rec['fullname'],
							'nickname':rec['nickname'],
							'rombel':rec['rombel'],
							'rayon':rec['rayon'],
							'gender':rec['gender'],
							'organisasi':rec['organisasi'],
							'password':rec['password'],
							'delete':False
						}})
				else:
					sd = mongo.db.users.count()
					print(sd)
					dict['_id'] = ObjectId()
					dict['nis'] = rec['nis']
					dict['auto'] = sd + 1
					dict['fullname'] = rec['fullname']
					dict['nickname'] = rec['nickname']
					dict['rombel'] = rec['rombel']
					dict['rayon'] = rec['rayon']
					dict['gender'] = rec['gender']
					dict['organisasi'] = rec['organisasi']
					dict['password'] = rec['password']
					dict['delete'] = False
					print('else')
					# print(dict)
					print(rec)
					mongo.db.users.insert(dict)
			flash('Success!')
	return render_template('uploadOp.html',data=tb,had=head)









# DASHBOARD
@app.route('/dashboard',methods=['POST','GET'])
def Dashboard():
	if 'login' in session:
		records = mongo.db.event.find()
	else:
		return redirect(url_for('Login'))
	return render_template('base.html',records=records)



@app.route('/event/<ids>',methods=['POST','GET'])
def delEvent(ids):
	delEvnt = mongo.db.event.remove({'_id':ObjectId(ids)})
	return redirect(url_for('Dashboard'))




@app.route('/siswa/delete/<ids>')
def delSiswa(ids):
	mongo.db.siswa.remove(ObjectId(ids))
	print('Messages  : Success Deleted')
	print(ids)
	a = flash('Success Deleted')
	return render_template('upload.html',msg=a)




@app.route('/edit/siswa/<ids>', methods=['GET','POST'])
def editSiswa(ids):
	data = mongo.db.siswa.find({'_id':ObjectId(ids)})
	rayon = mongo.db.rayon.find()
	if request.method=='POST':
		a = mongo.db.siswa.update({'_id':ObjectId(ids)},{'$set':request.form.to_dict()})
		return redirect(url_for('uploadSiswa'))
	return render_template('/admin/edit_siswa.html',data=data,rayon=rayon)




@app.route('/petugas/delete/<int:nis>')
def delPetugas(nis):
	mongo.db.users.remove({'nis':nis})
	print('Messages  : Success Deleted')
	a = flash('Success Deleted')
	return redirect(url_for('uploadCSV'))


@app.route('/absent/base/<ids>',methods=['GET','POST'])
def absent(ids):
	session['id'] = ids
	return render_template('/admin/absent.html', ids=ids)

@app.route('/absent/data', methods=['GET','POST'])
def absentD():
	if not request.form:
		print(session['id'])
		return render_template('/admin/absent.html')
	checkRombel = mongo.db.absent.count({'rombel':request.form['find']})
	if checkRombel == 0 and request.method=='POST':
		had = ['Nis','name','Rombel','Rayon']
		tbc = mongo.db.absent.count({'eventId':ObjectId(session['id']),'rayon':request.form['find']})
		find = mongo.db.absent.find({'eventId':ObjectId(session['id']),'rayon':request.form['find']})
	else:
		had = ['Nis','Fullname','Rombel','Rayon']
		tbc = mongo.db.absent.count({'eventId':ObjectId(session['id']),'rombel':request.form['find']})
		find = mongo.db.absent.find({'eventId':ObjectId(session['id']),'rombel':request.form['find']})
	return render_template('/admin/absent.html', records=find,had=had,jml=tbc)




# LOGOUT
@app.route('/logout',methods=['POST','GET'])
def LogOut():
	session.pop('login', None)
	return redirect(url_for('Login'))












#Eror 404
@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404