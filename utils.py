
import sqlite3
from typing import Counter




class Dbconnect:

    def __init__(self, path):
        self.connect = sqlite3.connect(path)
        self.cursos = self.connect.cursor()


    def __del__(self):
        self.cursos.close()
        self.connect.close()


    def get_by_title(title):
        db_connect = Dbconnect('netflix.db')
        db_connect.cursos.execute(
            f"""
            SELECT title, country, release_year, listed_in, description 
            FROM netflix 
            WHERE title LIKE '%{title}%'
            ORDER BY release_year DESC
            LIMIT 1
            """
)
        result = db_connect.cursos.fetchone()
        return {
		"title": result[0],
		"country": result[1],
		"release_year": result[2],
		"genre": result[3],
		"description": result[4]
}

    def get_by_year(year_one, year_two):
        db_connect = Dbconnect('netflix.db')
        db_connect.cursos.execute(
            f"""
            SELECT release_year, title 
            FROM netflix 
            WHERE release_year 
            BETWEEN {year_one} AND {year_two} 
            LIMIT 100
            """
)
        result = db_connect.cursos.fetchall()
        result_list = []
        for title in result:
            result_list.append({"title":title[1],
	                            "release_year": title[0]})
        return result_list
	    
	    
    def get_by_rating(rating):
        db_connect = Dbconnect('netflix.db')
        rating_parametrs = {
            "children": "'G'",
            "family": "'G', 'PG', 'PG-13'",
            "adult": "'R', 'NC-17'"
        }
        if rating not in rating_parametrs:
            return "Такой категорий нет"
            
        query = f"SELECT rating, title, description FROM netflix WHERE rating in ({rating_parametrs[rating]})"
        db_connect.cursos.execute(query)

        result = db_connect.cursos.fetchall()
        result_list = []

        for title in result:
            result_list.append(
                [
	{
	 "title":title[1],
	 "rating": title[0],
	 "description":title[2]
	}	
                ]
            )
        return result_list


    def get_by_genre(genre):
        db_connect = Dbconnect('netflix.db')
        db_connect.cursos.execute(
            f"""
            SELECT title, description 
            FROM netflix 
            WHERE listed_in LIKE '{genre}' 
            ORDER BY listed_in DESC 
            LIMIT 10
        """
        )

        result = db_connect.cursos.fetchall()
        result_list = []

        for title in result:
            result_list.append(
                [
	{
	 "title":title[0],
	 "description":title[1]
	}	
                ]
            )
        return result_list


    def get_by_actors(actor_one, actor_two):
        db_connect = Dbconnect('netflix.db')
        db_connect.cursos.execute(f"SELECT `cast` FROM netflix WHERE `cast` LIKE '%{actor_one}%'AND `cast` LIKE '%{actor_two}%'")
        result = db_connect.cursos.fetchall()
        actors_list = []

        for cast in result:
            actors_list.extend(cast[0].split(', '))
        counter = Counter(actors_list)
        result_list = []
        for actor, count in counter.items():
            if actor not in [actor_one, actor_two] and count > 2:
                result_list.append(actor)
        return result_list
        

    def get_by_type(type, year, genre):
        db_connect = Dbconnect('netflix.db')
        db_connect.cursos.execute(
            f"""
            SELECT title, description  
            FROM netflix 
            WHERE type = '{type}' 
            AND release_year LIKE '%{year}%' 
            AND listed_in LIKE '%{genre}%'
            """
        )

        result = db_connect.cursos.fetchall()

        result_list = []

        for title in result:
            result_list.append(
                
	{
	 "title":title[0],
	 "description":title[1]
	}	
                
            )
        return result_list

