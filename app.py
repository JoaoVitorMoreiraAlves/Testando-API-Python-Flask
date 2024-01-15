from flask import Flask, request, make_response, jsonify
import mysql.connector

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


host = "roundhouse.proxy.rlwy.net"
port = 46219
user = "root"
password = "ABbHa2fg52gh3gHD13bFcfAFHa3AE45F"
database = "railway"


# Agora você pode usar a variável 'conn' para executar consultas SQL

@app.route('/busca_usuarios', methods=['GET'])
def busca():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        query = 'SELECT * FROM usuarios'
        cursor.execute(query)

        # Recupere os resultados da consulta
        data = cursor.fetchall()

        #Tratando os dados
        resposta = []
        for data_array in data:
            item = {
                "id":data_array[0],
                "nick":data_array[1],
                "login":data_array[2],
                "senha":data_array[3],
                "email":data_array[4],
                "saldo":data_array[5],
                "status":data_array[6],
                "data_nasc":data_array[7],
                "vitoria":data_array[8],
                "derrota":data_array[9]
            }
            resposta.append(item)
        # Fechando o cursor e a conexão com o banco de dados
        cursor.close()
        conn.close()

        #Devolvendo a resposta
        return make_response(
            jsonify(resposta)
        ) 
    except Exception as erro:
        return jsonify({"error": str(erro)})


@app.route('/cria_usuario', methods=['POST'])
def cria_usuario():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        pessoa = request.json

        query = (f"CALL registra_jogador ('{pessoa['nick']}', '{pessoa['login']}', '{pessoa['senha']}', '{pessoa['email']}', '{pessoa['data_nasc']}')")
        cursor.execute(query)
        conn.commit()

        # Fechando o cursor e a conexão com o banco de dados
        cursor.close()
        conn.close()

        return make_response(
            jsonify(
                mensagem='Pessoa cadastrada com sucesso!',
                pessoa=pessoa
            )
        )
    except Exception as erro:
        return jsonify({"error": str(erro)})


@app.route('/cancela_usuario', methods=['PUT'])
def cancela_usuario():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        pessoa = request.json
        
        query = f"Call cancela_jogador({pessoa['id']})"
        cursor.execute(query)
        conn.commit()

        # Fechando o cursor e a conexão com o banco de dados
        cursor.close()
        conn.close()

        return make_response(
            jsonify(
                mensagem='Pessoa cancelada com sucesso!',
            )
        )
    except Exception as erro:
        return jsonify({"error": str(erro)})


@app.route('/login', methods=['GET'])
def login():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        login = request.args.get('login')
        senha = request.args.get('senha')

        if login is None or senha is None:
            return make_response(jsonify({"error": "Parâmetros 'login' e 'senha' são obrigatórios."}))
        
        query = f"CALL login('{login}','{senha}')"
        cursor.execute(query)
        result = cursor.fetchall()

        if (result[0][0] == 1):
            return make_response(
            jsonify(
                mensagem = "Login Realizado com Sucesso!"
                )
            )
        elif (result[0][0] == 0):
            return make_response(
                jsonify(
                    error = "Login errado ou inexistente!"
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})


@app.route('/compra_skin', methods=['POST'])
def compra_skin():
    try:
        #Conectando no banco de dados
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        #Pegando os valores pelo json
        pessoa_skin = request.json
        
        #Chamando a procedure para realizar a compra da Skin
        compra = f"CALL compra_skin({pessoa_skin['id']},{pessoa_skin['id_skin']}, @erro)"
        cursor.execute(compra)

        result = cursor.fetchone()
        
        if result[0] == 1:
            #Caso o resultado dar 1 significa que o usuário não tem saldo suficiente para comprar a skin
            return make_response(
                jsonify(
                    error = "Saldo Insuficiente!"
                )
            )
        elif result[0] == 2:
            #Caso o resultado seja 2 significa que ocorreu algum erro na hora de realizar a compra da skin(saldo não foi gasto)
            return make_response(
                jsonify(
                    error = "Erro ao realizar a compra do usuário !"
                )
            )
        else:
            #Compra realizada com Sucesso! Foi debitado do saldo do usuário o valor da skin
            return make_response(
                jsonify(
                    mensagem = "Skin comprada com Sucesso!"
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})
    
@app.route('/troca_skin', methods=['PUT'])
def troca_skin():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        pessoa_skin = request.json


        query = f"CALL troca_skin({pessoa_skin['id']},{pessoa_skin['id_skin']})"
        cursor.execute(query)
        conn.commit()
        
        return make_response(
                jsonify(
                    mensagem = "Skin trocada com Sucesso!"
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})


@app.route('/visualiza_skin_pessoal', methods=['GET'])
def visualiza_skin_pessoal():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        id = request.args.get('id')

        if id is None:
            return make_response(jsonify({"error": "Parâmetros 'id' é obrigatório."}))
        
        query = f"CALL visualiza_skins({id})"
        cursor.execute(query)
        result = cursor.fetchall()

        skins_dict = {}

        for i, (skin_name,) in enumerate(result):
            skin_key = f"Skin{i + 1}"
            skins_dict[skin_key] = skin_name

        return make_response(
                jsonify(
                    skins_dict
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})


@app.route('/abrir_loja', methods=['GET'])
def abrir_loja():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        query = "CALL visualiza_loja"
        cursor.execute(query)
        msg = cursor.fetchall()

        #Tratando os dados
        resposta = []
        for data_array in msg:
            item = {
                "id":data_array[0],
                "nome":data_array[1],
                "preco":data_array[2],
                "tipo":data_array[3]
            }
            resposta.append(item)

        return make_response(
                jsonify(
                    resposta
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})
    



@app.route('/pega_nick', methods=['GET'])
def pega_nick():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        login = request.args.get('login')

        if login is None:
            return make_response(jsonify({"error": "Parâmetros 'login' é obrigatório."}))

        query = f"CALL pega_nick('{login}')"
        cursor.execute(query)

        result = cursor.fetchall()

        msg = {"Nick": result[0][0]}
        
        return make_response(
                jsonify(
                    msg
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})


@app.route('/insert_partida', methods=['POST'])
def insert_partida():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        partida = request.json
        
        query = f"CALL insert_partida({partida['id1']}, {partida['id2']})"
        cursor.execute(query)

        result = cursor.fetchall()

        # Converter a lista de listas em um formato JSON específico
        msg = {
                "id_partida": result[0][0],
                "Status": result[0][1],
                "Vencedor": result[0][2],
                "id_jogador1": result[0][3],
                "id_jogador2": result[0][4]
            }

        return make_response(
                jsonify(
                    msg
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})



@app.route('/consulta_status_partida', methods=['GET'])
def consulta_status_partida():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        id_partida = request.args.get('id_partida')

        if id_partida is None:
            return make_response(jsonify({"error": "Parâmetros 'id_partida' é obrigatório."}))
        
        query = f"CALL consulta_status_partida({id_partida})"
        cursor.execute(query)

        result = cursor.fetchall()

        msg = {
            "Status": result[0][0],
            "Vencedor": result[0][1]
        }
        return make_response(
                jsonify(
                    msg
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})
    


@app.route('/atualiza_partida', methods=['PUT'])
def atualiza_partida():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        partida = request.json

        query = f"CALL atualiza_partida({partida['id_partida']}, {partida['id_vencedor']})"
        cursor.execute(query)
        result = cursor.fetchall()

        # Converter a lista de listas em um formato JSON específico
        msg = {
                "id_partida": result[0][0],
                "Status": result[0][1],
                "Vencedor": result[0][2],
                "id_jogador1": result[0][3],
                "id_jogador2": result[0][4]
        }

        return make_response(
                jsonify(
                    msg
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})



@app.route('/atualiza_senha', methods=['PUT'])
def atualiza_senha():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        pessoa = request.json

        query = f"CALL atualiza_senha({pessoa['id_pessoa']}, '{pessoa['senhaNova']}', '{pessoa['senhaAntiga']}')"
        cursor.execute(query)

        result = cursor.fetchall()

        if (pessoa['senhaNova'] != result[0][3]):
            return make_response(
                jsonify(
                    error = "Senha Antiga inválida!"
                )
            )
        elif (pessoa['senhaNova'] == result[0][3]):
            return make_response(
                jsonify(
                    mensagem = "Troca de Senha Realizada Com Sucesso!"
                )
            )
           
    except Exception as erro:
        return jsonify({"error": str(erro)})


@app.route('/pega_id', methods=['GET'])
def pega_id():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        nick = request.args.get('nick')

        if nick is None:
            return make_response(jsonify({"error": "Parâmetros 'nick' é obrigatório."}))
        
        query = f"CALL pega_id('{nick}')"
        cursor.execute(query)

        result = cursor.fetchall()

        msg = {
            "id": result[0][0]
        }

        return make_response(
                jsonify(
                    msg
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})




@app.route('/att_vencedor_perdedor', methods=['PUT'])
def att_vencedor_perdedor():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        partida = request.json

        query = f"CALL att_vencedor_perdedor({partida['id_vencedor']}, {partida['id_perdedor']})"

        cursor.execute(query)

        resposta = []

        results = cursor.fetchall()
        for result in results:
            msg = {
                "id_usuario": result[0],
                "nick": result[1],
                "vitoria": result[2],
                "derrota": result[3]
            }  
            resposta.append(msg)

        return make_response(
                jsonify(
                    resposta
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})
    

@app.route('/fazer_recarga', methods=['PUT'])
def fazer_recarga():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        usuario = request.json

        try:
            query = f"CALL fazer_recarga({usuario['id']}, {usuario['saldo']})"
            cursor.execute(query)
            conn.commit()
        except Exception as erro:
            return jsonify({"error": str(erro)})
        
        return make_response(
                jsonify(
                    mensagem = "Recarga realizada com sucesso!"
                )
            )
    except Exception as erro:
        return jsonify({"error": str(erro)})
    

@app.route('/recupera_senha', methods=['GET'])
def recupera_senha():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        Login = request.args.get('Login')
        
        if Login is None:
            return make_response(jsonify({"error": "Parâmetros 'Login' e 'email' é obrigatório."}))
        
        query = f"CALL verifica_email('{Login}')"
        cursor.execute(query)

        result = cursor.fetchall()

        if result:
            if result[0][6] == "Cancelado":
                return make_response(
                    jsonify(
                        error = "Essa conta está Cancelada!"
                    )
                )
            else:
                import random
                import string

                # Defina os caracteres que você deseja usar na senha (letras maiúsculas, minúsculas e dígitos)
                caracteres = string.ascii_letters + string.digits

                # Gere uma senha de 8 dígitos
                senha = ''.join(random.choice(caracteres) for _ in range(8))

                # Fechar o cursor antes de executar a segunda chamada
                cursor.close()

                conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
                cursor = conn.cursor()

                query = f"CALL att_senha_esquecida('{Login}', '{senha}')"
                cursor.execute(query)

                msg = {"SenhaNova": senha}
                return make_response(
                        jsonify(
                            msg
                        )
                    )
        else:
            return make_response(
                    jsonify(
                        error = "Login informado errado!"
                    )
                )
    except Exception as erro:
        return jsonify({"error": str(erro)})
    



#Crud para o superuser mecher nas skins
@app.route('/inserir_skin_superuser', methods=['POST'])
def inserir_skin_superuser():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        usuario_skin = request.json
        
        query = f"CALL inserir_skin_superuser('{usuario_skin['login']}', '{usuario_skin['senha']}', '{usuario_skin['nomeSkin']}', {usuario_skin['preco_skin']}, '{usuario_skin['tipo_skin']}', @result);"

        cursor.execute(query)

        cursor.execute("SELECT @result;")
        result = cursor.fetchall()[0]

        conn.commit()

        # Retorna o resultado para o cliente
        if result[0] == 2:
            return make_response(jsonify(error = "Credencias inválidas!"))
        elif result[0] == 3:
            return make_response(jsonify(error = "Usuario Informado não existe!"))
        elif result[0] == 1:
            return make_response(jsonify(mensagem = "Skin inseriada com Sucesso!"))
        else:
            return make_response(jsonify(error = "Erro por algum motivo desconhecido! Por Favor informe a área de TI!"))

    except Exception as erro:
        return jsonify({"error": str(erro)})
    


@app.route('/excluir_skin_superuser', methods=['DEL'])
def excluir_skin_superuser():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        usuario_skin = request.json
        
        query = f"CALL excluir_skin_superuser('{usuario_skin['login']}', '{usuario_skin['senha']}', '{usuario_skin['nomeSkin']}', {usuario_skin['preco_skin']}, '{usuario_skin['tipo_skin']}', @result);"

        cursor.execute(query)

        cursor.execute("SELECT @result;")
        result = cursor.fetchall()[0]

        conn.commit()

        # Retorna o resultado para o cliente
        if result[0] == 2:
            return make_response(jsonify(error = "Credencias inválidas!"))
        elif result[0] == 3:
            return make_response(jsonify(error = "Usuario Informado não existe!"))
        elif result[0] == 4:
            return make_response(jsonify(error = "Skin Informada não Existe!"))
        elif result[0] == 1:
            return make_response(jsonify(mensagem = "Skin excluida com Sucesso!"))
        else:
            return make_response(jsonify(error = "Erro por algum motivo desconhecido! Por Favor informe a área de TI!"))

    except Exception as erro:
        return jsonify({"error": str(erro)})




@app.route('/atualizar_skin_superuser', methods=['PUT'])
def atualizar_skin_superuser():
    try:
        conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()

        usuario_skin = request.json
        
      
        query = f"CALL att_skin_superuser('{usuario_skin['login']}', '{usuario_skin['senha']}', {usuario_skin['id_skin']}, '{usuario_skin['nomeSkin']}', {usuario_skin['preco_skin']}, '{usuario_skin['tipo_skin']}', @result);"
        cursor.execute(query)

        cursor.execute("SELECT @result;")
        result = cursor.fetchall()[0]

        # Retorna o resultado para o cliente
        if result[0] == 2:
            return make_response(jsonify(error = "Credencias inválidas!"))
        elif result[0] == 3:
            return make_response(jsonify(error = "Usuario Informado não existe!"))
        elif result[0] == 4:
            return make_response(jsonify(error = "Skin Informada não Existe!"))
        elif result[0] == 1:
            return make_response(jsonify(mensagem = "Skin atualizada com Sucesso!"))
        else:
            return make_response(jsonify(error = "Erro por algum motivo desconhecido! Por Favor informe a área de TI!"))
        
    except Exception as erro:
        return jsonify({"error": str(erro)})
    
if __name__ == '__main__':
    app.run(debug=True)