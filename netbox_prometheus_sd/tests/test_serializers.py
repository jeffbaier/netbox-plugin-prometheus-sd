from django.test import TestCase

from ..api.serializers import (
    PrometheusDeviceSerializer,
    PrometheusIPAddressSerializer,
    PrometheusVirtualMachineSerializer,
)
from . import utils


class PrometheusVirtualMachineSerializerTests(TestCase):
    def test_vm_minimal_to_target(self):

        instance = utils.build_minimal_vm("vm-01.example.com")
        data = PrometheusVirtualMachineSerializer(many=True, instance=[instance]).data[0]

        self.assertEqual(data["targets"], ["vm-01.example.com"])
        self.assertDictContainsSubset({"__meta_netbox_id": str(instance.id)}, data["labels"])
        self.assertDictContainsSubset(
            {"__meta_netbox_model": "VirtualMachine"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_status": "active"}, data["labels"]
        )
        self.assertDictContainsSubset({"__meta_netbox_cluster": "DC1"}, data["labels"])
        self.assertDictContainsSubset(
            {"__meta_netbox_cluster_group": "VMware"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_cluster_type": "On Prem"}, data["labels"]
        )

    def test_vm_full_to_target(self):
        instance = utils.build_vm_full("vm-full-01.example.com")
        data_list = PrometheusVirtualMachineSerializer(many=True, instance=[instance]).data

        self.assertEqual(data_list[0]["targets"], ["vm-full-01.example.com:4242"])
        self.assertDictContainsSubset(
            {"__metrics__path__": "/not/metrics"}, data_list[0]["labels"]
        )
        self.assertDictContainsSubset(
            {"__scheme__": "https"}, data_list[0]["labels"]
        )
        self.assertEqual(data_list[0]["targets"], ["vm-full-01.example.com:4242"])

        self.assertEqual(data_list[1]["targets"], ["vm-full-01.example.com:4243"])
        for data in data_list:
            self.assertDictContainsSubset({"__meta_netbox_id": str(instance.id)}, data["labels"])
            self.assertDictContainsSubset(
                {"__meta_netbox_model": "VirtualMachine"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_status": "active"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_tenant": "Acme Corp."}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_tenant_slug": "acme"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_site": "Campus A"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_site_slug": "campus-a"}, data["labels"]
            )
            self.assertDictContainsSubset({"__meta_netbox_role": "VM"}, data["labels"])
            self.assertDictContainsSubset({"__meta_netbox_role_slug": "vm"}, data["labels"])
            self.assertDictContainsSubset(
                {"__meta_netbox_platform": "Ubuntu 20.04"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_platform_slug": "ubuntu-20.04"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_primary_ip": "2001:db8:1701::2"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_primary_ip4": "192.168.0.1"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_primary_ip6": "2001:db8:1701::2"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_custom_field_simple": "Foobar 123"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_custom_field_int": "42"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_custom_field_bool": "True"}, data["labels"]
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_custom_field_json": "{'foo': ['bar', 'baz']}"},
                data["labels"],
            )
            self.assertDictContainsSubset(
                {"__meta_netbox_custom_field_multi_selection": "['foo', 'baz']"},
                data["labels"],
            )
            self.assertDictContainsSubset(
                {
                    "__meta_netbox_custom_field_contact":
                    "[{'id': 1, 'url': 'http://localhost:8000/api/tenancy/contacts/1/',"
                        + " 'display': 'Foo', 'name': 'Foo'}]"
                },
                data["labels"],
            )
            self.assertDictContainsSubset(
                {
                    "__meta_netbox_custom_field_text_long":
                    "This is\r\na  pretty\r\nlog\r\nText"
                },
                data["labels"],
            )


class PrometheusDeviceSerializerTests(TestCase):
    def test_device_minimal_to_target(self):
        instance = utils.build_minimal_device("firewall-01")
        data = PrometheusDeviceSerializer(many=True, instance=[instance]).data[0]

        self.assertEqual(data["targets"], ["firewall-01"])
        self.assertDictContainsSubset({"__meta_netbox_id": str(instance.id)}, data["labels"])
        self.assertDictContainsSubset({"__meta_netbox_model": "Device"}, data["labels"])
        self.assertDictContainsSubset(
            {"__meta_netbox_role": "Firewall"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_role_slug": "firewall"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_device_type": "SRX"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_device_type_slug": "srx"}, data["labels"]
        )
        self.assertDictContainsSubset({"__meta_netbox_site": "Site"}, data["labels"])
        self.assertDictContainsSubset(
            {"__meta_netbox_site_slug": "site"}, data["labels"]
        )

    def test_device_config_context_no_array(self):
        instance = utils.build_device_config_context_no_array("firewall-no-array-01")
        data = PrometheusDeviceSerializer(many=True, instance=[instance]).data[0]

        self.assertEqual(data["targets"], ["firewall-no-array-01:4242"])

    def test_device_config_context_invalid_1(self):
        instance = utils.build_device_config_context_invalid_1("firewall-invalid-01")
        data = PrometheusDeviceSerializer(many=True, instance=[instance]).data[0]

        self.assertEqual(data["targets"], ["firewall-invalid-01"])

    def test_device_config_context_invalid_2(self):
        instance = utils.build_device_config_context_invalid_2("firewall-invalid-02")
        data = PrometheusDeviceSerializer(many=True, instance=[instance]).data[0]

        self.assertEqual(data["targets"], ["firewall-invalid-02"])

    def test_device_config_context_mix_valid_invalid(self):
        instance = utils.build_device_config_context_mix_invalid_valid("firewall-valid-invalid-01")
        data = PrometheusDeviceSerializer(many=True, instance=[instance]).data[0]

        self.assertEqual(data["targets"], ["firewall-valid-invalid-01:4242"])

    def test_device_full_to_target(self):
        instance = utils.build_device_full("firewall-full-01")
        data = PrometheusDeviceSerializer(many=True, instance=[instance]).data[0]

        self.assertEqual(data["targets"], ["firewall-full-01"])
        self.assertDictContainsSubset({"__meta_netbox_id": str(instance.id)}, data["labels"])
        self.assertDictContainsSubset({"__meta_netbox_model": "Device"}, data["labels"])
        self.assertDictContainsSubset(
            {"__meta_netbox_platform": "Junos"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_platform_slug": "junos"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_primary_ip": "2001:db8:1701::2"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_primary_ip4": "192.168.0.1"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_primary_ip6": "2001:db8:1701::2"}, data["labels"]
        )
        self.assertDictContainsSubset({"__meta_netbox_rack": "R01B01"}, data["labels"])
        self.assertDictContainsSubset(
            {"__meta_netbox_tenant": "Acme Corp."}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_tenant_slug": "acme"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_custom_field_simple": "Foobar 123"}, data["labels"]
        )


class PrometheusIPAddressSerializerTests(TestCase):
    def test_ip_minimal_to_target(self):
        instance = utils.build_minimal_ip("10.10.10.10/24")
        data = PrometheusIPAddressSerializer(many=True, instance=[instance]).data[0]

        self.assertEqual(data["targets"], ["10.10.10.10"])
        self.assertDictContainsSubset({"__meta_netbox_id": str(instance.id)}, data["labels"])
        self.assertDictContainsSubset(
            {"__meta_netbox_status": "active"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_model": "IPAddress"}, data["labels"]
        )

    def test_ip_full_to_target(self):
        instance = utils.build_full_ip(
            address="10.10.10.10/24", dns_name="foo.example.com"
        )
        data = PrometheusIPAddressSerializer(many=True, instance=[instance]).data[0]

        self.assertEqual(
            data["targets"],
            ["foo.example.com"],
            "IP with DNS name should use DNS name as target",
        )
        self.assertDictContainsSubset({"__meta_netbox_id": str(instance.id)}, data["labels"])
        self.assertDictContainsSubset(
            {"__meta_netbox_status": "active"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_model": "IPAddress"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_ip": "10.10.10.10"},
            data["labels"],
            "IP should not have an subnet",
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_tenant": "Starfleet"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_tenant_slug": "starfleet"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_tenant_group": "Federation"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_tenant_group_slug": "federation"}, data["labels"]
        )
        self.assertDictContainsSubset(
            {"__meta_netbox_custom_field_simple": "Foobar 123"}, data["labels"]
        )
