

# Organizacion de Flask
#     Carpetas
#         -   templates/          van todos los archivos HTML
#         -   static/             van todos los archivos CSS Y JS


from flask import Flask, render_template,request, jsonify
import datetime
import Connection_sql


app = Flask(__name__)


@app.route('/Api/postulant')
def getAllPostulant():
    postulants=[]
    conn = Connection_sql.connectionServer('Origen')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.Postulants")
    for row in cursor.fetchall():
        postulants.append({
            "Id": row[0], 
            "Name": row[1],
            "First_Name": row[2], 
            "Second_Name": row[3], 
            "Age": row[4], 
            "Profession": row[5], 
            "Actual_State": row[6],
            "Date_Registration": row[7],
            "Date_Modify": row[8] 
        })
    conn.close()
    return(jsonify(postulants))

@app.route('/Api/postulant/<int:id>')
def getPostulant(id):
    codigoPostulante= id
    postulant=[]
    conn = Connection_sql.connectionServer('Origen')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM dbo.Postulants WHERE Id =" + str(codigoPostulante))
    for row in cursor.fetchall():
        postulant.append({
            "Id": row[0], 
            "Name": row[1],
            "First_Name": row[2], 
            "Second_Name": row[3], 
            "Age": row[4], 
            "Profession": row[5], 
            "Actual_State": row[6],
            "Date_Registration": row[7],
            "Date_Modify": row[8] 
        })
        print()
    conn.close()
    return(jsonify(postulant))

    #return('Trae Postulante  Especifico '+ str(codigoPostulante))
@app.route('/Api/postulant/<int:id>',methods=['DELETE'])
def deleteDeletePostulant(id):
    codigoPostulante= id
    conn = Connection_sql.connectionServer('Origen')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Postulants WHERE Id = " +str(codigoPostulante))
    cursor.commit()
    conn.close()
    return ('Postulante Eliminado'+ str(codigoPostulante))


@app.route('/Api/postulant',methods=['POST'])
def postSavePostulant():
    conn = Connection_sql.connectionServer('Origen')
    dateNow = datetime.datetime.now()
    date = "%s/%s/%s" % (dateNow.year, dateNow.month,dateNow.day) 
    print (str(dateNow))
    cursor = conn.cursor()
    queryInsertPostulant =  ''' 
                                SET NOCOUNT ON;
                                INSERT INTO Postulants 
                                VALUES (?,?,?,?,?,?,?,?);
                                SELECT @@IDENTITY AS ID;   
                            '''
    cursor.execute  (queryInsertPostulant,
                        (   
                            request.json['Name'],
                            request.json['First_Name'],
                            request.json['Second_Name'],
                            request.json['Age'],
                            request.json['Profession'],
                            request.json['Actual_State'],
                            date,
                            dateNow
                        )
                    )    
    id = cursor.fetchone()[0]
    print(id)  

    queryInsertPostulant =  ''' 
                                SET NOCOUNT ON;
                                INSERT INTO State_Change 
                                VALUES (?,'Sin Definir',?,'New into Postulant');
                                SELECT @@IDENTITY AS ID;   
                            '''
    cursor.execute  (queryInsertPostulant,
                        (   
                            id,
                            dateNow
                        )
                    ) 
    id = cursor.fetchone()[0]
    print(id)  

    cursor.commit()
    conn.close()
    return ('Postulante Agregado')
    #return('Guarda Informacion del Postulante')


@app.route('/Api/postulant',methods=['PUT'])
def putUpdatePostulant():
    codigoPostulante= str(request.json['Id'])
    print(codigoPostulante)
    dateNow = datetime.datetime.now()
    conn = Connection_sql.connectionServer('Origen')
    cursor = conn.cursor()
    sqlQuery =  ''' 
                    UPDATE A SET 
                        A.Name=? ,
                        A.First_Name=? ,
                        A.Second_Name=? ,
                        A.Age=?,
                        A.Profession=?,
                        A.Date_Modificate=?
                    FROM Postulants A WHERE A.Id = ?
                '''
    cursor.execute(sqlQuery ,(
                                (request.json['Name']),
                                (request.json['First_Name']),
                                (request.json['Second_Name']),
                                (request.json['Age']),
                                (request.json['Profession']),
                                dateNow,
                                str(codigoPostulante)
                            )
                    )
    cursor.commit()
    conn.close()
    return ('Postulante Modificado'+ str(codigoPostulante))


@app.route('/Api/postulant/reason',methods=['POST'])
def putUpdatePostulantReason():
    codigoPostulante= str(request.json['Id'])
    dateNow = datetime.datetime.now()
    date = "%s/%s/%s" % (dateNow.year, dateNow.month,dateNow.day) 

    print(codigoPostulante)
    conn = Connection_sql.connectionServer('Origen')

    cursor = conn.cursor()
    sqlQuery =  ''' 
                    UPDATE A SET 
                        A.Actual_State=?
                    FROM Postulants A WHERE A.Id = ?
                '''
    cursor.execute(sqlQuery ,(
                                (request.json['State']),
                                str(codigoPostulante)
                            )
                    )

    cursor = conn.cursor()
    sqlQuery =  ''' 
                    SET NOCOUNT ON;
                    INSERT INTO State_Change 
                    VALUES (?,?,?,?);
                    SELECT @@IDENTITY AS ID;
                '''
    cursor.execute(sqlQuery ,(
                                str(codigoPostulante),
                                (request.json['State']),
                                dateNow,
                                (request.json['Reason'])
                            )
                    )


    cursor.commit()
    conn.close()
    return ('Postulante Modificado'+ str(codigoPostulante))

@app.route('/')
def main():

    return render_template('index.html')

if __name__ == '__main__':
    app.run(None,3000,True)

