from database.Contiguity import Contiguity
from database.Country import Country
from database.DB_connect import DBConnect


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def read_countries() -> list[Country]:
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary = True)
        query = "SELECT * FROM country;"

        cursor.execute(query)
        l = []
        for row in cursor.fetchall():
            l.append(Country(
                abbreviation=row["StateAbb"],
                code=row["CCode"],
                full_name=row["StateNme"]
            ))

        cursor.close()
        cnx.close()
        return l

    @staticmethod
    def read_contiguities(max_year: int) -> list[Contiguity]:
        """
        Read all the contiguities with the specified max_year and return only the ones
        matching also the type, with detailed informations of the countries already loaded
        """
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """
        SELECT c.state1no as ca_statecode, c.state2no as cb_statecode, c.year, ca.StateAbb as ca_stateabb, 
ca.StateNme as ca_statename, cb.StateAbb as cb_stateabb, cb.StateNme as cb_statename 
FROM contiguity c, country ca, country cb
	WHERE c.`year` <= %s AND
		c.conttype = 1 AND
		ca.CCode = c.state1no AND
		cb.CCode  = c.state2no;
        """

        data = tuple([max_year])

        cursor.execute(query, data)
        results = []
        for row in cursor.fetchall():
            results.append(
                Contiguity(
                    country_code_a=row["ca_statecode"],
                    country_code_b=row["cb_statecode"],
                    country_a=Country(
                        code=row["ca_statecode"],
                        abbreviation=row["ca_stateabb"],
                        full_name=row["ca_statename"]
                    ),
                    country_b=Country(
                        code=row["cb_statecode"],
                        abbreviation=row["cb_stateabb"],
                        full_name=row["cb_statename"]
                    ),
                )
            )

        cursor.close()
        cnx.close()
        return results