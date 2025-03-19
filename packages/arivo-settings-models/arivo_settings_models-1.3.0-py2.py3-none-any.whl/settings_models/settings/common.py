from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import root_validator, validator, constr

from settings_models.validators import uuid_validator, domain_validator, account_id_range_validator
from settings_models._combat import SettingsModel, Field


class GateType(str, Enum):
    """
    Types of a gate. This defines the usage and the general behavior of a gate
    """

    entry = "entry"
    """Entry gate: Used where vehicles typically or exclusively enter the parking lot"""

    exit = "exit"
    """Exit gate: Used where vehicles typically or exclusively exit the parking lot"""

    bidirectional = "bidirectional"
    """Bidirectional gate: Used where vehicles typically enter AND exit the parking lot"""

    door = "door"
    """
    Door: Gate without LPR where people can walk into the parking lot. 
    No check-in or check-out, only access check
    """

    transit_access_check = "transit_access_check"
    """
    Gate with barrier where vehicles can pass depending on access rights specified by the gate list in parksetting or
    shortterm_gates in parking_area. This is a well defined functionality of the controller.
    """

    transit_custom = "transit_custom"
    """
    Gates with custom behavior. These gates might or might not have a barrier. Examples are: 
      - Passage check gates (permanent parkers must pass this gate or gets fined)
      - Gate with shortterm count check (e.g. only 10 shortterm parkers are allowed at the same time)
      - automatic gates (e.g. exit of restricted subarea)
    Behavior of those gates is not implemented by the controller
    """

    coupled_lane = "coupled_lane"
    """
    Gates which open always together with another lane (e.g. garage door after entry barrier) but can also be controlled
    independently, e.g. perma open
    """

    multilane = "multilane"
    """
    Gates where multiple vehicles can pass at the same (either in parallel or in opposite direction).
    This is only allowed in Freeflow mode and with no user interaction (e.g. display)
    """

    transit_multilane = "transit_multilane"
    """
    Multilane type of transit_custom (multiple vehicles can pass at the same). Only allowed for automatically setting
    something for passing vehicles (e.g. changing rate) 
    """


class RefsModel(SettingsModel):
    """
    Model for used keys of a Dict setting like parksettings
    """
    name: str = Field(..., description="Human readable name of the service using the keys for error messages",
                      max_length=126)
    keys: List[str] = Field(..., description="Keys referenced by the service")


class Gate(SettingsModel):
    """
    Definition of a Gate
    """
    gate: constr(min_length=1, max_length=126, regex=r"^[a-z0-9\-_]+$") = \
        Field(..., description="Technical name of gate")
    name: str = Field(..., description="Name for UIs", max_length=126)
    type: GateType = Field(..., description="Type of the gate. Defines the usage and general behavior")
    opposite_gate: Optional[str] = Field(None, description="Name of the opposite gate for bidirectional gates")


class Rate(SettingsModel):
    """
    Definition of a parking rate
    """
    rate_yaml: str = Field(..., description="Parking rate config: https://gitlab.com/accessio/onegate/parking-rates")
    name: str = Field(..., description="Name for UIs", max_length=126)
    id: str = Field(..., description="id for referencing of this rate")

    id_validator = uuid_validator("id")


class CommandCostEntryTypes(str, Enum):
    """
    Types of command cost entries: Those are used to cost entries in a parking session, e.g. via parksettings
    """

    static_cost = "static_cost"
    """static cost immediately booked"""

    pending_static_cost = "pending_static_cost"
    """static cost booked at exit"""

    rate_change = "rate_change"
    """for rate changes that don't generate revenue reduction entry"""

    rate_validation = "rate_validation"
    """for rate changes that generate revenue reduction entry (usually reducing costs)"""

    partial_rate_change = "partial_rate_change"
    """for rate changes which freeze costs until now"""

    amount_validation = "amount_validation"
    """validation for up to a certain amount"""

    time_validation = "time_validation"
    """validation for a certain time"""

    payment = "payment"
    """payment"""

    cost_validation = "cost_validation"
    """generates a validation (gen_revenue_reduction) for open costs in group"""

    disable_costs = "disable_costs"
    """cancels costs in group (either disable before booking or gen_cancellation)"""

    cancel_remaining_costs = "cancel_remaining_costs"
    """generates cancellation over remaining amount for each group"""

    payoff_costs = "payoff_costs"
    """generates pay off over (set to 0 remaining when session not editable) for each group"""

    free_timerange = "free_timerange"
    """
    instead of calculating dynamic costs from start to end, 
    we calculate them from start to free_timerange start + free_timerange end to end
    """


class CostEntryData(SettingsModel):
    """
    Defines a cost entry command, which is for example set at entering the parking lot
    """
    entry_type: CommandCostEntryTypes = Field(..., description="Cost entry command type")
    value: Optional[Union[int, str, Dict[str, Optional[datetime]]]] = (
        Field(None, description="value: Dependent on entry_type it's an int, a str or None"))
    group: Optional[str] = Field(None, description="Cost group the command cost entry is applied on. None for global")
    account_id: str = Field(..., description="The account_id the generated booked cost entry will be booked at. "
                                             "It is an integer between 0 and 3999 formatted as string")

    account_id_validator = account_id_range_validator("account_id", 0, 3999)

    # Not used in settings, set by service applying the command cost entry (e.g. access service)
    source: Optional[str]
    source_id: Optional[str]
    idempotency_key: Optional[str]

    @root_validator(skip_on_failure=True)
    def data_validation(cls, values):
        if values.get("entry_type") in [CommandCostEntryTypes.static_cost, CommandCostEntryTypes.pending_static_cost,
                                        CommandCostEntryTypes.amount_validation, CommandCostEntryTypes.time_validation,
                                        CommandCostEntryTypes.payment]:
            if not isinstance(values["value"], int) or values["value"] <= 0:
                raise ValueError("value must be an integer greater 0")
        elif values.get("entry_type") in [CommandCostEntryTypes.rate_change, CommandCostEntryTypes.rate_validation,
                                          CommandCostEntryTypes.partial_rate_change]:
            values["value"] = str(values["value"])
        if values.get("entry_type") not in [CommandCostEntryTypes.payment, CommandCostEntryTypes.cancel_remaining_costs,
                                            CommandCostEntryTypes.payoff_costs, CommandCostEntryTypes.free_timerange]:
            if values["group"] is None:
                raise ValueError("group must be set")
        elif values.get("entry_type") in [CommandCostEntryTypes.cancel_remaining_costs,
                                          CommandCostEntryTypes.payoff_costs]:
            if values["group"] is not None:
                raise ValueError("group must NOT be set")
        elif values.get("entry_type") == CommandCostEntryTypes.free_timerange:
            values["value"] = dict(entry_start=values["value"].get("entry_start"),
                                   entry_end=values["value"].get("entry_end"))
            if values["group"] is None:
                raise ValueError("group must be set")
        return values


class ShorttermLimitType(str, Enum):
    """
    Types of shortterm limits
    """
    no_limit = "no_limit"
    """no limit"""

    shortterm_count = "shortterm_count"
    """number of shortterm parkers in area is compared to limit"""

    total_count = "total_count"
    """number of all parkers in area are compared to limit"""


class ParkingArea(SettingsModel):
    """
    Defines a physical area of the whole parking lot by specifying the gates of types entry, exit, bidirectional or
    transit_barrier/transit_access_check. Also defines which gates allow shortterm parkers, the default cost entries
    for unknown parkers and pay-per-use parkers and limits for shortterm parkers in this area.
    This is the config for counters and shortterm parkers (registered and unregistered)
    """
    id: str = Field(..., description="Id of the parking area. UUID string in canonical textual representation")
    name: str = Field(..., description="Name for UIs", max_length=126)
    gates: List[str] = Field(..., description="Gates in this physical area (only types entry, exit, bidirectional or "
                                              "transit_barrier/transit_access_check)", min_items=1)
    shortterm_gates: List[str] = Field(..., description="Gates in this physical area (only types entry, exit, "
                                                        "bidirectional or transit_barrier/transit_access_check), where "
                                                        "shortterm parkers are allowed")
    default_cost_entries: List[CostEntryData] = Field(..., description="Default cost entries added on entry in this "
                                                                       "parking area for unknown parkers")
    pay_per_use_cost_entries: Optional[List[CostEntryData]] = \
        Field(None, description="Default cost entries added on entry in this parking area for pay-per-use parkers. None"
                                " is fallback to default_cost_entries")
    shortterm_limit_type: ShorttermLimitType = Field(..., description="Type of shortterm limit")
    shortterm_limit: int = Field(..., description="Limit value in this area. Compared to value specified in "
                                                  "shortterm_limit_type", ge=0)

    id_validator = uuid_validator("id")

    @validator('default_cost_entries', each_item=True)
    def cost_entry_validator(cls, cost_entry):
        if cost_entry.entry_type in [CommandCostEntryTypes.partial_rate_change, CommandCostEntryTypes.payment,
                                     CommandCostEntryTypes.cancel_remaining_costs, CommandCostEntryTypes.payoff_costs]:
            raise ValueError(f"{cost_entry.entry_type} is not allowed as default cost entry in parking area")
        return cost_entry

    @validator('pay_per_use_cost_entries', each_item=True)
    def pay_per_use_cost_entries_validator(cls, cost_entry):
        if cost_entry.entry_type in [CommandCostEntryTypes.partial_rate_change, CommandCostEntryTypes.payment,
                                     CommandCostEntryTypes.cancel_remaining_costs, CommandCostEntryTypes.payoff_costs]:
            raise ValueError(f"{cost_entry.entry_type} is not allowed as pay per use cost entry in parking area")
        return cost_entry

    @root_validator(skip_on_failure=True)
    def validate_shortterm_gates_in_gates(cls, values):
        """
        check if all shortterm gates are in gates
        """
        if not all(gate in values["gates"] for gate in values["shortterm_gates"]):
            raise ValueError("All shortterm gates must be in gates")
        if len(values["shortterm_gates"]) == 0 and len(values["default_cost_entries"]) > 0:
            raise ValueError("If no shortterm gates are defined, no default cost entries are allowed")
        return values


class Parksetting(SettingsModel):
    """
    Defines the terms and conditions for parking sessions of registered users. This is not used for registered
    shortterm parkers.
    """
    id: str = Field(..., description="Id of the parksetting. UUID string in canonical textual representation")
    name: str = Field(..., description="Name for UIs", max_length=126)
    gates: List[str] = Field(..., description="Gates this parksetting is valid for (only types entry, exit, "
                                              "bidirectional or transit_barrier/transit_access_check", min_items=1)
    default_cost_entries: List[CostEntryData] = Field(..., description="Default cost entries added on entry. "
                                                                       "Empty list is free.")

    id_validator = uuid_validator("id")

    @validator('default_cost_entries', each_item=True)
    def cost_entry_validator(cls, cost_entry):
        if cost_entry.entry_type in [CommandCostEntryTypes.partial_rate_change, CommandCostEntryTypes.payment,
                                     CommandCostEntryTypes.cancel_remaining_costs, CommandCostEntryTypes.payoff_costs]:
            raise ValueError(f"{cost_entry.entry_type} is not allowed as default cost entry in parksetting")
        return cost_entry


class CostGroup(SettingsModel):
    """
    Definition of cost group, specifying name, account_id and VAT rate.
    """
    id: str = Field(..., description="Id of the cost group. Scheme of this ID see "
                                     "https://youtrack.acc.si/youtrack/articles/DEV-A-1080#kostengruppen")
    name: str = Field(..., description="Name for UIs", max_length=126)
    account_id: str = Field(..., description="The account_id set in cost entries using this cost group (only costs)"
                                             "It is an integer between 0 and 3999 formatted as string")
    vat_rate: float = Field(..., ge=0.0, le=100.0, description="VAT rate of this cost group in %")

    account_id_validator = account_id_range_validator("account_id", 0, 999)

    @root_validator(skip_on_failure=True)
    def data_validation(cls, values):
        """
        check if cost group id prefix matches account_id range
        """
        # validator is run before root_validator, so int cast is safe
        if int(values["account_id"]) < 100 and not values["id"].startswith("parking_"):
            raise ValueError("account_ids from 0 to 99 must have cost_group id parking_*")
        if 100 <= int(values["account_id"]) < 200 and not values["id"].startswith("fine_"):
            raise ValueError("account_ids from 100 to 199 must have cost_group id fine_*")
        if 200 <= int(values["account_id"]) < 300 and not values["id"].startswith("ev-charging_"):
            raise ValueError("account_ids from 200 to 299 must have cost_group id ev-charging_*")
        if 300 <= int(values["account_id"]) < 400 and not values["id"].startswith("honest-payment_"):
            raise ValueError("account_ids from 300 to 399 must have cost_group id honest-payment_*")
        if 400 <= int(values["account_id"]) < 500 and not values["id"].startswith("misc_"):
            raise ValueError("account_ids from 400 to 499 must have cost_group id misc_*")
        return values


class PrivacyTime(SettingsModel):
    """
    Model to define timespan as used in privacy settings. At least one of minutes, hours, days must > 0
    """
    minutes: int = Field(0, ge=0, description="Miuntes of timespan. Must be >= 0 if given")
    hours: int = Field(0, ge=0, description="Hours of timespan. Must be >= 0 if given")
    days: int = Field(0, ge=0, description="Days of timespan. Must be >= 0 if given")

    @root_validator(skip_on_failure=True)
    def data_validation(cls, values):
        if values["minutes"] == 0 and values["hours"] == 0 and values["days"] == 0:
            raise ValueError("At least one of minutes, hours or days must be > 0")
        return values


class PrivacySettings(SettingsModel):
    """
    Settings for data anonymization in the parking system (on the device)
    """
    paid: PrivacyTime = Field(..., description="For parking sessions with all costs paid")
    unpaid: PrivacyTime = Field(..., description="For parking sessions with unpaid costs")
    registered_free: PrivacyTime = Field(..., description="For parking sessions with a free parking permission")
    pay_via_invoice: PrivacyTime = Field(..., description="For parking sessions which are paid later via invoice")
    open: PrivacyTime = Field(..., description="Unfinished parking sessions")
    free: PrivacyTime = Field(..., description="Data of customers which did not really use the parking lot "
                                               "(no costs, no registration)")
    honest_payment: PrivacyTime = Field(..., description="Data of honest payments")
    erroneous: PrivacyTime = Field(..., description="Data of erroneous incidents, e.g. unknown vehicle at the exit")
    rejected: PrivacyTime = Field(..., description="Data of rejections, where someone could not enter the parking lot")


class AddressModel(SettingsModel):
    """
    Address data, e.g. for billing address
    """
    name: str = Field(..., description="Name of entity at this address, e.g. provider name")

    street: str = Field(..., description="Street name")
    number: str = Field(..., description="House number")
    floor: Optional[str] = Field(None, description="Floor number or name")
    door: Optional[str] = Field(None, description="Door number or name")
    supplements: Optional[str] = Field(None, description="Additional description of address")

    city: str = Field(..., description="City")
    zip_code: str = Field(..., description="Zip code")
    state: Optional[str] = Field(None, description="State")
    country: str = Field(..., description="Country")


class BillingSettings(SettingsModel):
    """
    Settings for billing
    """
    vat_id: str = Field(..., description="VAT id of payment receiver")
    billing_address: AddressModel = Field(..., description="Address payment receiver")


class Location(AddressModel):
    """
    Address data with coordinates, e.g. for garage location
    """
    longitude: float = Field(..., description="Longitude of location")
    latitude: float = Field(..., description="Latitude of location")


class SupportSettings(SettingsModel):
    """
    Contact data for support cases (e.g. shown at signs, displays or end user UIs).
    Support means questions to contracts or complaints against costs and NOT emergency calls
    (cannot enter door, cannot pay, ...)
    """
    name: str = Field(..., description="Name of the person/entity responsible for support, e.g. provider")
    address: Optional[AddressModel] = Field(None, description="Address for written support letters")
    phone_number: Optional[constr(min_length=3, max_length=32, regex=r"^\+[0-9 ]+$")] = \
        Field(None, description="Phone number for support (not emergency calls)")
    email_address: Optional[constr(min_length=3, max_length=254,
                                   regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")] = \
        Field(None, description="Email address for support")
    website: Optional[constr(min_length=3, max_length=1022)] = Field(None, description="Website for support")

    @root_validator(skip_on_failure=True)
    def data_validation(cls, values):
        if (values["address"] or values["phone_number"] or values["email_address"] or values["website"]) is None:
            raise ValueError("At least one of address, phone_number, email_address or website must be given")
        return values


class GarageModes(str, Enum):
    """
    Garage modes
    """
    barrier = "barrier"
    """Standard barrier mode for commercial parking lots (barriers at entries and exits)"""

    freeflow = "freeflow"
    """Standard freeflow mode for commercial parking lots (no barriers at all)"""

    freeflow_surveillance = "freeflow_surveillance"
    """Surveillance only freeflow mode. No payments. Just observation of parking lot"""

    barrier_bypass = "barrier_bypass"
    """Bypass barrier mode, where unregistered parkers are handled by a third-party system"""


class GarageSettings(SettingsModel):
    """
    General garage settings defining general behavior of parking lot. Contains mode and flags for features which are
    enabled/disabled depending on the mode
    """
    mode: GarageModes = Field(..., description="General parking lot mode, e.g. freeflow. This field is more for "
                                               "information in UI and setup than for real technical use.")
    honest_payment_enabled: bool = Field(False, description="If honest payments are allowed")
    enforcement_enabled: bool = Field(False, description="If unpaid parking sessions can be enforced")
    payment_possible: bool = Field(False, description="If any parking system payments (Kiosk, PayApp,...) are possible")

    @root_validator(skip_on_failure=True, pre=True)
    def data_validation(cls, values):
        if values["mode"] == GarageModes.freeflow:
            values["honest_payment_enabled"] = True
            values["enforcement_enabled"] = True
            values["payment_possible"] = True
        elif values["mode"] == GarageModes.barrier:
            values["honest_payment_enabled"] = False
            values["enforcement_enabled"] = False
            values["payment_possible"] = True
        elif values["mode"] == GarageModes.freeflow_surveillance:
            values["honest_payment_enabled"] = False
            values["enforcement_enabled"] = False
            values["payment_possible"] = False
        elif values["mode"] == GarageModes.barrier_bypass:
            values["honest_payment_enabled"] = False
            values["enforcement_enabled"] = False
            values["payment_possible"] = False
        return values


class GarageName(SettingsModel):
    """
    Names of Garage (directly set in Garage UI / iam)
    """
    name: str = Field(..., description="Name of Garage for UIs and end users", max_length=126)
    technical_name: constr(min_length=3, max_length=63, regex=r"^[a-z0-9\-]+$") = \
        Field(..., description="Technical/internal name of garage")
    slug: constr(min_length=3, max_length=126, regex=r"^[a-zA-Z0-9\-_]+$") = \
        Field(..., description="Shortname of Garage used in URLs")


class Urls(SettingsModel):
    """
    Collection of URLs used by various services (mainly for generating QRs or displaying links to user)
    """
    payapp_domain: str = Field(..., description="Domain of Arivo PayApp")
    payapp_short_url: str = Field(..., description="Full URL for PayApp with garage set")
    receipt_domain: str = Field(..., description="Domain of Arivo receipt website")

    payapp_domain_validator = domain_validator("payapp_domain")
    receipt_domain_validator = domain_validator("receipt_domain")


Gates = Dict[str, Gate]
Rates = Dict[str, Rate]
ParkingAreas = Dict[str, ParkingArea]
Parksettings = Dict[str, Parksetting]
CostGroups = Dict[str, CostGroup]
