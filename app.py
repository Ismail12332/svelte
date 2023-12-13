from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from passlib.hash import bcrypt
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from flask_cors import CORS
from werkzeug.utils import secure_filename 

load_dotenv()

def create_app():
    class User:
        def __init__(self, username, password, email):
            self.username = username
            self.password_hash = bcrypt.hash(password)
            self.email = email



    app = Flask(__name__, template_folder='templates')
    CORS(app)
    app.secret_key = "Jebn^$gdYGTHudjy%"
    client = MongoClient("mongodb://localhost:27017")
    app.db = client.my_database
    users_collection = app.db.users
    projects_collection = app.db.projects


    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            user = users_collection.find_one({"username": username})

            if user and bcrypt.verify(password, user["password_hash"]):
                session["user_id"] = str(user["_id"])
                print("User ID in session:", session["user_id"])
                return "Success"  # Возвращаем успешный ответ

            return "Incorrect username or password."

        return render_template("login.html")

    #выход
    @app.route("/logout")
    def logout():
        # Очищаем сессию пользователя при выходе
        session.pop("user_id", None)
        return redirect(url_for("login"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            email = request.form.get("email")

            # Проверка, что пользователь с таким именем уже не существует
            if users_collection.find_one({"username": username}):
                return "Пользователь с таким именем уже существует."

            # Создание нового пользователя и сохранение его в базе данных
            new_user = User(username, password, email)
            users_collection.insert_one({
                "username": new_user.username,
                "password_hash": new_user.password_hash,
                "email": new_user.email
            })

            return render_template("login.html")

        return render_template("register.html")


    @app.route("/index2", methods=["GET", "POST"])
    def home():
        user_id = session.get("user_id")
        
        # Проверяем, что пользователь вошел в систему
        if user_id is None:
            return redirect(url_for("login"))

        # Обновляем запрос к базе данных, чтобы фильтровать проекты по user_id
        projects = app.db.projects.find({"user_id": ObjectId(user_id)})

        if request.method == "POST":
            first_name = request.form.get("first_name")
            last_name = request.form.get("last_name")
            city = request.form.get("city")
            phone = request.form.get("phone")
            post = request.form.get("post")
            vessel_name = request.form.get("vessel_name")
            
            try:
                user_id = ObjectId(user_id)
            except Exception as e:
                return "Invalid user_id", 400

            # Создаем проект
            project = {
                "first_name": first_name,
                "last_name": last_name,
                "city": city,
                "phone": phone,
                "post": post,
                "sections": [],
                "vessel_name": vessel_name,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": user_id
            }

            result = app.db.projects.insert_one(project)
            project_id = result.inserted_id

            print("Entry added:", first_name, last_name, city, phone, post, vessel_name)
            return redirect(url_for('edit_project', project_id=project_id))
        

        return render_template("index2.html", projects=projects, user_id=user_id)



    #Переключение на проект в главное странице нажатие на имя проекта
    @app.route("/edit_project/<string:project_id>", methods=["GET"])
    def edit_project(project_id):
        try:
            project_id = ObjectId(project_id)  # Преобразовываем project_id в ObjectId
        except Exception as e:
            # Обработка ошибки, если project_id неверного формата
            return "Invalid project_id", 400

        user_id = session.get("user_id")

        # Проверяем, что текущий пользователь имеет доступ к проекту
        project = app.db.projects.find_one({"_id": project_id})
        if project is None:
            return "Project not found", 404

        # Преобразовываем user_id из сессии в ObjectId для сравнения
        user_id = ObjectId(user_id)

        # Сравниваем user_id из сессии с user_id в проекте
        if user_id != project.get("user_id"):
            return "Access denied", 403  # Возвращаем код 403 (Доступ запрещен)

        return render_template("edit_project.html", project=project, project_id=project_id)


    #Дабовление и удаление записей в разделах
    @app.route("/edit_project/<project_id>/add_step", methods=["POST"])
    def add_step(project_id):
        try:
            project_id = ObjectId(project_id)  # Преобразовываем project_id в ObjectId
        except Exception as e:
            # Обработка ошибки, если project_id неверного формата
            return "Invalid project_id", 400

        step_description = request.form.get("step_description")
        section = request.form.get("section")  # Получаем значение раздела из формы

        # Определите, в какой раздел добавить шаг
        section_field = f"{section}_steps"

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$push": {section_field: step_description}}
            )
            if result.modified_count == 0:
                # Если ни одна запись не была изменена, возможно, нет проекта с таким project_id
                return "Project not found", 404
        except Exception as e:
            # Обработка других ошибок, например, проблем с базой данных
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id, current_section=section))


    @app.route("/edit_project/<project_id>/delete_step", methods=["POST"])
    def delete_step(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        step_to_delete = request.form.get("step_to_delete")
        section = request.form.get("section")
        project = app.db.projects.find_one({"_id": project_id})
        
        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$pull": {f"{section}_steps": step_to_delete}}
            )
            if result.modified_count == 0:
                return "Project not found", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        # После успешного удаления шага, перенаправьтесь обратно в текущий раздел
        return redirect(url_for("edit_project", project_id=project_id, current_section=section))


    #----------------------------------------------------------------
    #Добавление раздела
    @app.route("/edit_project/<project_id>/add_section", methods=["POST"])
    def add_section(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        section_name = request.form.get("section_name")

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$push": {"sections": {"name": section_name, "subsections": []}}}
            )
            if result.modified_count == 0:
                return "Project not found", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))


    #--удаление раздела
    @app.route("/edit_project/<project_id>/delete_section/<section_name>", methods=["POST"])
    def delete_section(project_id, section_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {"$pull": {"sections": {"name": section_name}}}
            )
            if result.modified_count == 0:
                return "Section not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))


    #Добавление подраздела
    @app.route("/edit_project/<project_id>/add_subsection", methods=["POST"])
    def add_subsection(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        section_name = request.form.get("section_name")
        subsection_name = request.form.get("subsection_name")

        try:
            result = app.db.projects.update_one(
                {"_id": project_id, "sections.name": section_name},
                {"$push": {"sections.$.subsections": {"name": subsection_name, "cells": []}}}
            )
            if result.modified_count == 0:
                return "Section not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))

    #--удаление подраздела
    @app.route("/edit_project/<project_id>/delete_subsection/<section_name>/<subsection_name>", methods=["POST"])
    def delete_subsection(project_id, section_name, subsection_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            result = app.db.projects.update_one(
                {"_id": project_id, "sections.name": section_name},
                {"$pull": {"sections.$.subsections": {"name": subsection_name}}}
            )
            if result.modified_count == 0:
                return "Subsection not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))


    #Добавление ячейки
    @app.route("/edit_project/<project_id>/add_cell", methods=["POST"])
    def add_cell(project_id):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        section_name = request.form.get("section_name")
        subsection_name = request.form.get("subsection_name")
        cell_name = request.form.get("cell_name")
        cell_description = request.form.get("cell_description")

        try:
            result = app.db.projects.update_one(
                {"_id": project_id},
                {
                    "$push": {
                        "sections.$[section].subsections.$[subsection].cells": {
                            "name": cell_name,
                            "description": cell_description
                        }
                    }
                },
                array_filters=[
                    {"section.name": section_name},
                    {"subsection.name": subsection_name}
                ]
            )
            if result.modified_count == 0:
                return "Section or subsection not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))



    #--удаление ячейки
    @app.route("/edit_project/<project_id>/delete_cell/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def delete_cell(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            # Находим проект по идентификатору
            project = app.db.projects.find_one({"_id": project_id})

            # Находим раздел, подраздел и ячейку, которую нужно удалить
            section_index = None
            subsection_index = None
            cell_index = None

            for i, section in enumerate(project["sections"]):
                if section["name"] == section_name:
                    section_index = i
                    for j, subsection in enumerate(section["subsections"]):
                        if subsection["name"] == subsection_name:
                            subsection_index = j
                            for k, cell in enumerate(subsection["cells"]):
                                if cell["name"] == cell_name:
                                    cell_index = k

            # Если раздел, подраздел и ячейка найдены, удаляем ячейку
            if section_index is not None and subsection_index is not None and cell_index is not None:
                del project["sections"][section_index]["subsections"][subsection_index]["cells"][cell_index]

                # Обновляем документ проекта в базе данных
                app.db.projects.update_one({"_id": project_id}, {"$set": project})

            else:
                return "Cell not found in the project", 404

        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))



    # -- удаление комментария
    @app.route("/edit_project/<project_id>/delete_comment/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def delete_comment(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            result = app.db.projects.update_one(
                {
                    "_id": project_id,
                    "sections.name": section_name,
                    "sections.subsections.name": subsection_name,
                    "sections.subsections.cells.name": cell_name
                },
                {
                    "$unset": {
                        "sections.$[section].subsections.$[subsection].cells.$[cell].comment": ""
                    }
                },
                array_filters=[
                    {"section.name": section_name},
                    {"subsection.name": subsection_name},
                    {"cell.name": cell_name}
                ]
            )
            if result.modified_count == 0:
                return "Section, subsection, or cell not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))
        


    #Добавление коментария
    @app.route("/edit_project/<project_id>/add_comment/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def add_comment(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        cell_comment = request.form.get("cell_comment")

        try:
            result = app.db.projects.update_one(
                {
                    "_id": project_id,
                    "sections.name": section_name,
                    "sections.subsections.name": subsection_name,
                    "sections.subsections.cells.name": cell_name
                },
                {
                    "$set": {
                        "sections.$[section].subsections.$[subsection].cells.$[cell].comment": cell_comment
                    }
                },
                array_filters=[
                    {"section.name": section_name},
                    {"subsection.name": subsection_name},
                    {"cell.name": cell_name}
                ]
            )
            if result.modified_count == 0:
                return "Section, subsection, or cell not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))



    # #--удаление рейтинга
    @app.route("/edit_project/<project_id>/delete_rating/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def delete_rating(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        try:
            # Находим проект по идентификатору
            project = app.db.projects.find_one({"_id": project_id})

            # Находим раздел, подраздел, ячейку и рейтинг, который нужно удалить
            section_index = None
            subsection_index = None
            cell_index = None
            rating_index = None

            for i, section in enumerate(project["sections"]):
                if section["name"] == section_name:
                    section_index = i
                    for j, subsection in enumerate(section["subsections"]):
                        if subsection["name"] == subsection_name:
                            subsection_index = j
                            for k, cell in enumerate(subsection["cells"]):
                                if cell["name"] == cell_name:
                                    cell_index = k
                                    if "rating" in cell:
                                        rating_index = "rating"

            # Если раздел, подраздел, ячейка и рейтинг найдены, удаляем рейтинг
            if (
                section_index is not None
                and subsection_index is not None
                and cell_index is not None
                and rating_index is not None
            ):
                del project["sections"][section_index]["subsections"][subsection_index]["cells"][cell_index][rating_index]

                # Обновляем документ проекта в базе данных
                app.db.projects.update_one({"_id": project_id}, {"$set": project})

            else:
                return "Rating not found in the project", 404

        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))
        


    #Добавление рейтинга
    @app.route("/edit_project/<project_id>/add_rating/<section_name>/<subsection_name>/<cell_name>", methods=["POST"])
    def add_rating(project_id, section_name, subsection_name, cell_name):
        try:
            project_id = ObjectId(project_id)
        except Exception as e:
            return "Invalid project_id", 400

        cell_rating = request.form.get("cell_rating")

        try:
            result = app.db.projects.update_one(
                {
                    "_id": project_id,
                    "sections.name": section_name,
                    "sections.subsections.name": subsection_name,
                    "sections.subsections.cells.name": cell_name
                },
                {
                    "$set": {
                        "sections.$[section].subsections.$[subsection].cells.$[cell].rating": cell_rating
                    }
                },
                array_filters=[
                    {"section.name": section_name},
                    {"subsection.name": subsection_name},
                    {"cell.name": cell_name}
                ]
            )
            if result.modified_count == 0:
                return "Section, subsection, or cell not found in the project", 404
        except Exception as e:
            print("Error:", e)
            return "An error occurred", 500

        return redirect(url_for("edit_project", project_id=project_id))

    if __name__ == "__main__":
        app.run(debug=True)
    
    return app
