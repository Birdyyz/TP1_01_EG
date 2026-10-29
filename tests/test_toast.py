from histo import parse_histoql, HistoQLSyntaxError
import unittest


class TestToAST(unittest.TestCase):

    def test_basic_query(self):
        result = parse_histoql(
            'FIND people RETURN name;'
        )

        self.assertEqual(result["kind"], "program")
        query = result["statements"][0]["query"]

        self.assertEqual(query["kind"], "query")
        self.assertEqual(query["entity"], "people")
        self.assertEqual(query["clauses"], [])
        self.assertEqual(query["return"], ["name"])

    def test_query_without_return(self):
        result = parse_histoql('FIND events;')
        query = result["statements"][0]["query"]

        self.assertEqual(query["entity"], "events")
        self.assertEqual(query["return"], ["name"])

    def test_multiple_return_fields(self):
        result = parse_histoql(
            'FIND people RETURN name, occupation;'
        )
        query = result["statements"][0]["query"]

        self.assertEqual(
            query["return"], ["name", "occupation"]
        )

    def test_during_clause(self):
        result = parse_histoql(
            'FIND people DURING 1800..1850 RETURN name;'
        )
        query = result["statements"][0]["query"]

        self.assertEqual(
            query["clauses"],
            [{
                "kind": "during",
                "start": 1800,
                "end": 1850
            }]
        )

    def test_place_clause(self):
        result = parse_histoql(
            'FIND people IN "Portugal" RETURN name;'
        )
        query = result["statements"][0]["query"]

        self.assertEqual(
            query["clauses"],
            [{"kind": "place", "value": "Portugal"}]
        )

    def test_where_clause(self):
        result = parse_histoql(
            'FIND people WHERE birth_year >= 1800 RETURN name;'
        )
        query = result["statements"][0]["query"]

        self.assertEqual(
            query["clauses"],
            [{
                "kind": "where",
                "field": "birth_year",
                "operator": ">=",
                "value": 1800
            }]
        )

    def test_relation_clause(self):
        result = parse_histoql(
            'FIND people WHO occupation "scientist" RETURN name;'
        )
        query = result["statements"][0]["query"]

        self.assertEqual(
            query["clauses"],
            [{
                "kind": "relation",
                "predicate": "occupation",
                "value": "scientist"
            }]
        )

    def test_let_statement(self):
        result = parse_histoql(
            'LET researchers = FIND people RETURN name;'
        )
        statement = result["statements"][0]

        self.assertEqual(statement["kind"], "let")
        self.assertEqual(statement["name"], "researchers")
        self.assertEqual(statement["query"]["entity"], "people")

    def test_exists_condition(self):
        result = parse_histoql(
            'IF EXISTS researchers { FIND people; }'
        )
        statement = result["statements"][0]

        self.assertEqual(statement["kind"], "if")
        self.assertEqual(
            statement["condition"],
            {"kind": "exists", "name": "researchers"}
        )

    def test_count_condition(self):
        result = parse_histoql(
            'IF people COUNT >= 2 { FIND people; }'
        )
        statement = result["statements"][0]

        self.assertEqual(
            statement["condition"],
            {
                "kind": "count_compare",
                "name": "people",
                "operator": ">=",
                "value": 2
            }
        )

    def test_foreach_statement(self):
        result = parse_histoql(
            'FOR EACH person IN researchers { FIND people; }'
        )
        statement = result["statements"][0]

        self.assertEqual(statement["kind"], "foreach")
        self.assertEqual(statement["item"], "person")
        self.assertEqual(statement["collection"], "researchers")
        self.assertEqual(len(statement["body"]), 1)

    def test_research_block(self):
        result = parse_histoql(
            'RESEARCH "Historical study" { FIND people; }'
        )

        self.assertEqual(result["kind"], "research")
        self.assertEqual(result["title"], "Historical study")
        self.assertEqual(len(result["statements"]), 1)

    def test_invalid_syntax(self):
        with self.assertRaises(HistoQLSyntaxError):
            parse_histoql('FIND people RETURN name')


if __name__ == "__main__":
    unittest.main(verbosity=2)
