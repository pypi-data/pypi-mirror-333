from netbox_network_importer.connections.Netbox import Netbox
from netbox_network_importer.helper import (
    canonical_interface_name_edited,
    get_diff,
)
from netbox_network_importer.results.results import Action, NetboxResult, Status


def process_bandwidth_interfaces(host, converted_bandwidth_ifcs) -> list:
    RESULTS = []  # list of NetboxResult

    # Init connection to Netbox via PyNetbox
    nb = Netbox.connect()

    # find the device instance in netbox
    dev = nb.dcim.devices.get(host.data["id"])

    # find interfaces linked to the device
    ifcs_filter = nb.dcim.interfaces.filter(device_id=dev.id)

    # convert filtered interfaces into dictionary of pynetbox interface instances
    nb_interfaces_dict = {
        canonical_interface_name_edited(ifc.name): ifc
        for ifc in [ifc for ifc in ifcs_filter]
    }

    # setup NB parameters
    for ifc, bandwidth in converted_bandwidth_ifcs.items():
        # get NB interface instance
        nb_ifc = nb_interfaces_dict.get(ifc, None)

        if nb_ifc:
            # Skip IGNORED interfaces
            if nb_ifc.custom_fields.get("ignore_importer", False) == True:
                RESULTS.append(
                    NetboxResult(
                        result=f"{nb_ifc.name} - Ignored by Importer - Skipping",
                        status=Status.SKIPPED,
                        action=Action.LOOKUP,
                        diff="",
                    )
                )

                nb_interfaces_dict.pop(nb_ifc.name, None)
                continue
            else:
                # If interface already exists in netbox, update it
                RESULTS.append(
                    interface_bandwidth_update(
                        nb_ifc=nb_ifc, bandwidth=bandwidth)
                )
        else:
            RESULTS.append(
                NetboxResult(
                    result=f"Interface {ifc} not found in Netbox",
                    status=Status.ERROR,
                    action=Action.LOOKUP,
                    diff={},
                )
            )
    return RESULTS


def interface_bandwidth_update(nb_ifc, bandwidth):
    try:
        # Get data before changes
        before = nb_ifc.custom_fields["bandwidth"]

        if nb_ifc.update({"custom_fields": {"bandwidth": bandwidth}}):
            nb_ifc = nb_ifc.api.dcim.interfaces.get(nb_ifc.id)
            after = nb_ifc.custom_fields["bandwidth"]

            return NetboxResult(
                result=f"{nb_ifc.name} - saved successfully",
                status=Status.CHANGED,
                action=Action.UPDATE,
                diff=get_diff(before, after),
            )
        else:
            return NetboxResult(
                result=f"{nb_ifc.name} - nothing to do",
                action=Action.UPDATE,
                status=Status.NOT_CHANGED,
                diff={},
            )
    except Exception as e:
        return NetboxResult(
            result=f"{nb_ifc.name} - Exception Occurs: {e}",
            status=Status.EXCEPTION,
            action=Action.DELETE,
            diff={},
            exception=e,
        )
