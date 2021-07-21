from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from flask import Flask, render_template, request
from wtforms import SubmitField
from application import app, db
from application.classes import Motherboard,CPU,ComputerCase, Build
from application.classes import CreateCaseEntry,CreateCPUEntry,CreateMotherBoardEntry,CreateBuildEntry,ReadBuildEntry,UpdateBuildEntry

@app.route('/add',methods=['GET','POST'])
def add():
    error=""   
    build_form=CreateBuildEntry()
    if request.method=="POST":
        build_name=build_form.name.data
        builddata=Build().query.filter_by(name=build_name).first()
        if builddata is not None and builddata.name==build_name:
            error="Build name already exists!"
        elif build_form.validate():
            new_build=Build(name=build_name)
            db.session.add(new_build)
            db.session.commit()
            error='Build name added successfully!'
    return render_template('addLayout.html',build_form=build_form,message=error)

@app.route('/add/motherboard',methods=['GET','POST'])
def addMotherboard():
    motherboard_form=CreateMotherBoardEntry()
    error=""

    if request.method=="POST":
        #Motherboard Entry configuration:
        build_name=motherboard_form.build_name.data
        motherboard_keyType=motherboard_form.keyType.data
        motherboard_make=motherboard_form.make.data
        motherboard_model=motherboard_form.model.data
        motherboard_series=motherboard_form.series.data
  
        builddata=Build().query.filter_by(name=build_name).first()
        if builddata is None:
            error="Build name doesnt exist.. Try again!"
        elif  motherboard_form.validate():
            new_motherboard_entry=Motherboard(keyType=motherboard_keyType,make=motherboard_make,model=motherboard_model,
            series=motherboard_series,build=Build.query.filter_by(name=build_name).first())
            db.session.add(new_motherboard_entry)
            db.session.commit()

            error = 'Added new motherboard'
        else: error = 'Failed to submit!'
    return render_template('addMotherboard.html',motherboard_form=motherboard_form,message=error)

@app.route('/add/cpu',methods=['GET','POST'])
def addCPU():
    cpu_form=CreateCPUEntry()
    error=""
    if request.method=="POST":
        #CPU Entry configuration:
        build_name=cpu_form.build_name.data
        cpu_make=cpu_form.make.data
        cpu_series=cpu_form.series.data
        cpu_model=cpu_form.model.data
        builddata=Build().query.filter_by(name=build_name).first()
        if builddata is None:
            error="Build name doesnt exist.. Try again!"
        elif cpu_form.validate():
            new_cpu_entry=CPU(make=cpu_make,series=cpu_series,model=cpu_model,build=Build.query.filter_by(name=build_name).first())
            db.session.add(new_cpu_entry)
            db.session.commit()
            error= "Added a CPU!"
        else: error= "Failed to add a CPU!"
    return render_template('addCPU.html',cpu_form=cpu_form,message=error)

@app.route('/add/case',methods=['GET','POST'])
def addCase():
    #Case Entry configuration:
    error=""
    case_form=CreateCaseEntry()
    if request.method=="POST":

        case_keyType=case_form.keyType.data
        case_make=case_form.make.data
        case_model=case_form.model.data
        build_name=case_form.build_name.data
        builddata=Build().query.filter_by(name=build_name).first()
        if builddata is None:
            error="Build name doesnt exist.. Try again!"
        elif case_form.validate():
            new_case_entry=ComputerCase(keyType=case_keyType,make=case_make,model=case_model,build=Build.query.filter_by(name=build_name).first())
            db.session.add(new_case_entry)
            db.session.commit()
            error = "Added a Case!"
        else: 
            error = "Failed to add a Case!"
    return render_template('addCase.html',case_form=case_form,message=error)    


@app.route('/',methods=['GET','POST'])
@app.route('/read',methods=['GET','POST'])
def read():
    error=''
    read_form=ReadBuildEntry()
    if request.method == 'POST':
        build_name=read_form.build_name.data
        builddata=Build().query.filter_by(name=build_name).first()
        if builddata is None:
            error="Build name doesnt exist.. Try again!"
        elif read_form.validate():
            builddata=Build().query.filter_by(name=build_name).first()
            mbdata=Motherboard().query.filter_by(build_id=builddata.id).first()
            cpudata=CPU().query.filter_by(build_id=builddata.id).first()
            casedata=ComputerCase().query.filter_by(build_id=builddata.id).first()
            error="This is your build:"
            if mbdata is not None: read_form.mb_name.data = mbdata.keyType + ' ' + mbdata.make + ' ' + mbdata.model + ' ' + mbdata.series
            if cpudata is not None: read_form.cpu_name.data = cpudata.make + ' ' + cpudata.model + ' ' + cpudata.series
            if casedata is not None: read_form.case_name.data = casedata.keyType + ' ' + casedata.make + ' ' + casedata.model
    return render_template('read.html',read_form=read_form,message=error)    

@app.route('/update',methods=['GET','POST'])
def update():
    error= ""
    update_form=UpdateBuildEntry()
    if request.method == 'POST':
        build_name=update_form.build_name.data
        new_build_name=update_form.new_build_name.data
        builddata=Build().query.filter_by(name=build_name).first()
        checkdata=Build().query.filter_by(name=new_build_name).first()
        if builddata is None:
            error="Build name doesnt exist.. Try again!"
        elif checkdata is not None and checkdata.name==new_build_name:
            error="There is another build using this name! Please try again."
        elif update_form.validate():
            builddata.name=new_build_name
            db.session.commit()
            error="Update the build name successfully!"
    return render_template('updateLayout.html',update_form=update_form,message=error)  

@app.route('/update/CPU',methods=['GET','POST'])
def updateCPU():
    cpu_form=CreateCPUEntry()
    error=""
    if request.method=="POST":
        #CPU Entry configuration:
        build_name=cpu_form.build_name.data
        cpu_make=cpu_form.make.data
        cpu_series=cpu_form.series.data
        cpu_model=cpu_form.model.data
        builddata=Build().query.filter_by(name=build_name).first()
        if builddata is not None:cpudata=CPU().query.filter_by(build_id=builddata.id).first()
        if builddata is None:
            error="Build name doesnt exist.. Try again!"
        elif cpudata is None:
            error="Couldn't find the desired CPU ensure it has been added!"
        elif cpu_form.validate():
            cpudata.make=cpu_make
            cpudata.series=cpu_series
            cpudata.model=cpu_model
            db.session.commit()
            error= "Updated the CPU!"
        else: error= "Failed to add a CPU!"
    return render_template('addCPU.html',cpu_form=cpu_form,message=error)

@app.route('/update/case',methods=['GET','POST'])
def updateCase():
    #Case Entry configuration:
    error=""
    case_form=CreateCaseEntry()
    if request.method=="POST":
        case_keyType=case_form.keyType.data
        case_make=case_form.make.data
        case_model=case_form.model.data
        build_name=case_form.build_name.data
        builddata=Build().query.filter_by(name=build_name).first()
        if builddata is not None:casedata=ComputerCase().query.filter_by(build_id=builddata.id).first()
        if builddata is None:
            error="Build name doesnt exist.. Try again!"
        elif casedata is None:
            error="Ensure you have added a case to this build!"
        elif case_form.validate():
            casedata.keyType=case_keyType
            casedata.make=case_make
            casedata.model=case_model
            db.session.commit()
            error = "Updated your case choice!"
        else: 
            error = "Failed to add a Case!"
    return render_template('addCase.html',case_form=case_form,message=error)    
@app.route('/update/motherboard',methods=['GET','POST'])
def updateMotherboard():
    motherboard_form=CreateMotherBoardEntry()
    error=""

    if request.method=="POST":
        #Motherboard Entry configuration:
        build_name=motherboard_form.build_name.data
        motherboard_keyType=motherboard_form.keyType.data
        motherboard_make=motherboard_form.make.data
        motherboard_model=motherboard_form.model.data
        motherboard_series=motherboard_form.series.data
  
        builddata=Build().query.filter_by(name=build_name).first()
        if builddata is not None: 
            mbdata=Motherboard().query.filter_by(build_id=builddata.id).first()
        if builddata is None:
            error="Build name doesnt exist.. Try again!"
        elif mbdata is None:
            error = "Ensure a motherboard was added to the build!"
        elif  motherboard_form.validate():
            mbdata.keyType=motherboard_keyType
            mbdata.make=motherboard_make
            mbdata.model=motherboard_model
            mbdata.series=motherboard_series
            db.session.commit()

            error = 'Updated your motherboard choice!'
        else: error = 'Failed to submit!'
    return render_template('addMotherboard.html',motherboard_form=motherboard_form,message=error)
