# Copyright 2019-present Kensho Technologies, LLC.
import unittest

import pytest

from ..macros import perform_macro_expansion
from .test_helpers import compare_graphql, get_schema, get_test_macro_registry


class MacroExpansionTests(unittest.TestCase):
    def setUp(self):
        """Disable max diff limits for all tests."""
        self.maxDiff = None
        self.schema = get_schema()
        self.macro_registry = get_test_macro_registry()
        self.type_equivalence_hints = {
            self.schema.get_type('Event'): self.schema.get_type('EventOrBirthEvent'),
        }

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_basic(self):
        query = '''{
            Animal {
                out_Animal_GrandparentOf {
                    name @output(out_name: "grandkid")
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                out_Animal_ParentOf {
                    out_Animal_ParentOf {
                        name @output(out_name: "grandkid")
                    }
                }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_non_leaf_target_and_field_merging(self):
        query = '''{
            Animal {
                out_Animal_RichYoungerSiblings {
                    net_worth @filter(op_name: "<", value: ["$net_worth_upper_bound"])
                              @output(out_name: "sibling_net_worth")
                }
            }
        }'''
        args = {
            'net_worth_upper_bound': 5,
        }

        expected_query = '''{
            Animal {
                net_worth @tag(tag_name: "net_worth")
                out_Animal_BornAt {
                    event_date @tag(tag_name: "birthday")
                }
                in_Animal_ParentOf {
                    out_Animal_ParentOf {
                        net_worth @filter(op_name: "<", value: ["$net_worth_upper_bound"])
                                  @filter(op_name: ">", value: ["%net_worth"])
                                  @output(out_name: "sibling_net_worth")
                        out_Animal_BornAt {
                            event_date @filter(op_name: "<", value: ["%birthday"])
                        }
                    }
                }
            }
        }'''
        expected_args = {
            'net_worth_upper_bound': 5,
        }

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_source_merging(self):
        query = '''{
            Animal {
                net_worth @filter(op_name: "<", value: ["$net_worth_upper_bound"])
                          @output(out_name: "net_worth")
                out_Animal_RichYoungerSiblings {
                    uuid
                }
            }
        }'''
        args = {
            'net_worth_upper_bound': 5,
        }

        expected_query = '''{
            Animal {
                net_worth @filter(op_name: "<", value: ["$net_worth_upper_bound"])
                          @output(out_name: "net_worth")
                          @tag(tag_name: "net_worth")
                out_Animal_BornAt {
                    event_date @tag(tag_name: "birthday")
                }
                in_Animal_ParentOf {
                    out_Animal_ParentOf {
                        net_worth @filter(op_name: ">", value: ["%net_worth"])
                        out_Animal_BornAt {
                            event_date @filter(op_name: "<", value: ["%birthday"])
                        }
                    }
                }
            }
        }'''
        expected_args = {
            'net_worth_upper_bound': 5,
        }

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_target_coercion_1(self):
        query = '''{
            Animal {
                out_Animal_AvailableFood {
                   ... on Food {
                       @output(out_name: "food")
                   }
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                out_Animal_LivesIn {
                    in_Entity_Related {
                        ... on Food {
                            @output(out_name: "food")
                        }
                    }
                }
            }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_target_coercion_2(self):
        query = '''{
            Animal {
                out_Animal_NearbyEvents {
                   ... on Event {
                       @output(out_name: "event")
                   }
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                out_Animal_LivesIn {
                    in_Entity_Related {
                        ... on Event {
                            @output(out_name: "event")
                        }
                    }
                }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_target_coercion_3(self):
        query = '''{
            Animal {
                out_Animal_NearbyEvents {
                   ... on BirthEvent {
                       @output(out_name: "event")
                   }
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                out_Animal_LivesIn {
                    in_Entity_Related {
                        ... on BirthEvent {
                            @output(out_name: "event")
                        }
                    }
                }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_target_coercion_4(self):
        query = '''{
            Animal {
                out_Animal_NearbyEntities {
                   ... on Event {
                       @output(out_name: "event")
                   }
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                out_Animal_LivesIn {
                    in_Entity_Related {
                        ... on Event {
                            @output(out_name: "event")
                        }
                    }
                }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_target_coercion_5(self):
        query = '''{
            Animal {
                out_Animal_NearbyEntities {
                   ... on Animal {
                       @output(out_name: "animal")
                   }
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                out_Animal_LivesIn {
                    in_Entity_Related {
                        ... on Animal {
                            @output(out_name: "animal")
                        }
                    }
                }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_target_coercion_with_filter_1(self):
        query = '''{
            Animal {
                out_Animal_NearbyEntities {
                   ... on Food @filter(op_name: "name_or_alias", value: "$wanted") {
                       @output(out_name: "animal")
                   }
                }
            }
        }'''
        args = {
            'wanted': 'croissant'
        }

        expected_query = '''{
            Animal {
                out_Animal_LivesIn {
                    in_Entity_Related {
                        ... on Food @filter(op_name: "name_or_alias", value: "$wanted"){
                            @output(out_name: "animal")
                        }
                    }
                }
            }
        }'''
        expected_args = {
            'wanted': 'croissant'
        }

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_target_coercion_with_filter_2(self):
        query = '''{
            Animal {
                out_Animal_NearbyEvents {
                   ... on BirthEvent @filter(op_name: "name_or_alias", value: ["$wanted"]){
                       @output(out_name: "event")
                   }
                }
            }
        }'''
        args = {
            'wanted': 'superbowl',
        }

        expected_query = '''{
            Animal {
                out_Animal_LivesIn {
                    in_Entity_Related {
                        ... on BirthEvent @filter(op_name: "name_or_alias", value: ["$wanted"]){
                            @output(out_name: "event")
                        }
                    }
                }
            }
        }'''
        expected_args = {
            'wanted': 'superbowl',
        }

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_target_coercion_with_filter_3(self):
        query = '''{
            Animal {
                out_Animal_GrandchildrenCalledNate {
                    name @output(out_name: "official_name")
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                out_Animal_ParentOf {
                    out_Animal_ParentOf @filter(op_name: "name_or_alias", value: ["$wanted"]) {
                        name @output(out_name: "grandkid")
                    }
                }
            }
        }'''
        expected_args = {
            'wanted': 'Nate',
        }

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_target_coercion_with_filter_4(self):
        query = '''{
            Animal {
                out_Animal_GrandchildrenCalledNate @filter(op_name: "name_or_alias",
                                                           value: ["$something"]) {
                    name @output(out_name: "official_name")
                }
            }
        }'''
        args = {
            'something': 'Peter',
        }

        expected_query = '''{
            Animal {
                out_Animal_ParentOf {
                    out_Animal_ParentOf @filter(op_name: "name_or_alias", value: ["$wanted"]) {
                                        @filter(op_name: "name_or_alias", value: ["$wanted"]) {
                        name @output(out_name: "grandkid")
                    }
                }
            }
        }'''
        expected_args = {
            'something': 'Peter',
            'wanted': 'Nate',
        }

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_arguments(self):
        query = '''{
            Location {
                name @filter(op_name: "=", value: ["$location"])
                out_Location_Orpans {
                    @output(out_name: "name")
                }
            }
        }'''
        args = {
            'location': 'Europe',
        }

        expected_query = '''{
            Location {
                name @filter(op_name: "=", value: ["$location"])
                in_Animal_LivesIn {
                    in_Animal_ParentOf @filter(op_name: "has_edge_degree", value: ["$num_parents"])
                                       @optional {
                        uuid
                    }
                }
            }
        }'''
        expected_args = {
            'location': 'Europe',
            'num_parents': 0,
        }

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_tag_collision(self):
        query = '''{
            Animal {
                net_worth @tag(tag_name: "parent_net_worth")
                out_Animal_RichSiblings {
                    @filter(op_name: ">", value: ["%parent_net_worth"])
                    name @output(out_name: "sibling")
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                net_worth @tag(tag_name: "parent_net_worth")
                in_Animal_ParentOf {
                    net_worth @tag(tag_name: "parent_net_worth_1")
                    out_Animal_ParentOf @macro_edge_target {
                        net_worth @filter(op_name: ">", value: ["%parent_net_worth_1"])
                        out_Animal_BornAt {
                            event_date @filter(op_name: "<", value: ["%birthday"])
                        }
                    }
                }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_edge_colocated_tags(self):
        query = '''{
            Animal {
                net_worth @tag(tag_name: "animal_net_worth")
                out_Animal_RichYoungerSiblings {
                    net_worth @filter(op_name: "<", value: ["%animal_net_worth"])
                              @output(out_name: "sibling_net_worth")
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                net_worth @tag(tag_name: "animal_net_worth")
                out_Animal_BornAt {
                    event_date @tag(tag_name: "birthday")
                }
                in_Animal_ParentOf {
                    out_Animal_ParentOf @macro_edge_target {
                        net_worth @filter(op_name: ">", value: ["%animal_net_worth"])
                        out_Animal_BornAt {
                            event_date @filter(op_name: "<", value: ["%birthday"])
                        }
                    }
                }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_nested_use(self):
        query = '''{
            Animal {
                out_Animal_GrandparentOf {
                    out_Animal_GrandparentOf {
                        name @output(out_name: "grandgrandkid")
                    }
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                out_Animal_ParentOf {
                    out_Animal_ParentOf {
                        out_Animal_ParentOf {
                            out_Animal_ParentOf {
                                name @output(out_name: "grandgrandkid")
                            }
                        }
                    }
                }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)

    @pytest.mark.skip(reason='not implemented')
    def test_macro_parallel_use(self):
        query = '''{
            Animal {
                out_Animal_GrandparentOf {
                   name @output(out_name: "grandkid")
                }
                out_Animal_ParentOf {
                    out_Animal_GrandparentOf {
                       name @output(out_name: "grandgrandkid")
                    }
                }
            }
        }'''
        args = {}

        expected_query = '''{
            Animal {
                out_Animal_ParentOf {
                    out_Animal_ParentOf {
                        name @output(out_name: "grandkid")
                    }
                }
                out_Animal_ParentOf {
                    out_Animal_ParentOf {
                        out_Animal_ParentOf {
                            name @output(out_name: "grandgrandkid")
                        }
                    }
                }
            }
        }'''
        expected_args = {}

        expanded_query, new_args = perform_macro_expansion(
            self.schema, self.macro_registry, query, args)
        compare_graphql(self, expected_query, expanded_query)
        self.assertEqual(expected_args, new_args)