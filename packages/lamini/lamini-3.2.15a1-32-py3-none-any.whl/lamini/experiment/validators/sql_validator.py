from lamini.experiment.validators import BaseSQLValidator

class SQLValidator(BaseSQLValidator):
    """Simple SQL validator that checks if a query can execute."""

    def __init__(
        self,
        model,
        db_type="sqlite",
        db_params=None,
        name="SQLValidator",
        sql_key="sql_query",  # key in prompt object data to get the SQL query from
        is_valid_field="is_valid",
        **kwargs,
    ):
        super().__init__(
            model=model,
            name=name,
            db_type=db_type,
            db_params=db_params,
            is_valid_field=is_valid_field,
            **kwargs,
        )

        self.sql_key = sql_key

        self.input[self.sql_key] = "str"

    def __call__(self, prompt_obj, debug=False):
        """
        Check if SQL query is valid by attempting to execute it.
        Note: This is a deterministic validator, so it does not call an LLM.
        It will look for the sql_key in the prompt object data.
        """
        if not prompt_obj.data.get(self.sql_key):
            prompt_obj.response = self.create_error_response("No SQL query provided")
            return prompt_obj

        query = prompt_obj.data[self.sql_key].strip()
        if not query:
            prompt_obj.response = self.create_error_response("Empty SQL query")
            return prompt_obj

        if not query.endswith(';'):
            query += ';'

        db_can_execute = False

        try:
            cursor = self.conn.cursor()
            cursor.execute(f"EXPLAIN QUERY PLAN {query}")
            prompt_obj.response = self.create_success_response()
            db_can_execute = True
        except Exception as e:
            prompt_obj.response = self.create_error_response(str(e))

        if not db_can_execute:
            new_query = self.fix_invalid_syntax(query)

            if new_query:
                if not new_query.endswith(';'):
                    new_query += ';'

                try:
                    cursor.execute(f"EXPLAIN QUERY PLAN {new_query}")
                    prompt_obj.data[self.sql_key] = new_query
                    prompt_obj.response = self.create_success_response()
                    db_can_execute = True
                except:
                    pass

        return prompt_obj

    def create_error_response(self, error_msg):
        """Create error response"""
        return {
            self.is_valid_field: False,
            "error": error_msg,
            "explanation": f"Query is invalid: {error_msg}"
        }

    def create_success_response(self):
        """Create success response"""
        return {
            self.is_valid_field: True,
            "error": None,
            "explanation": "Query is valid and can be executed"
        }

    def fix_invalid_syntax(self, query):
        i_codeblock = query.find('```')

        if i_codeblock != -1:
            query = query[i_codeblock:]

        queryl = query.lower()

        if not query.lower().startswith('with'):
            init_tokens = ['select', 'with']
            i_start = None

            for init_token in init_tokens:
                i_start = queryl.find(init_token)
                if i_start != -1:
                    break
                if not i_start:
                    return None

            query = query[i_start:]

        i_semicolon = query.find(';')

        if i_semicolon != -1:
            query = query[:i_semicolon + 1]

        return query