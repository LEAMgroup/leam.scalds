from zope.interface import Interface
# -*- Additional Imports Here -*-
from zope import schema

from leam.scalds import scaldsMessageFactory as _



class ISCALDS(Interface):
    """Interface to the SCALDS Model."""

    # -*- schema definition goes here -*-
    end_time = schema.Date(
        title=_(u"Model End Time"),
        required=False,
        description=_(u"Logs when model ends execution."),
    )
#
    start_time = schema.Date(
        title=_(u"Model Start Time"),
        required=False,
        description=_(u"Logs when the model begins execution."),
    )
#
    runstatus = schema.TextLine(
        title=_(u"Model Run Status"),
        required=True,
        description=_(u"Maintain the state of the job."),
    )
#
    water = schema.Object(
        title=_(u"Water and Sewer Costs"),
        required=False,
        description=_(u"A vector map providing costs associated with households/employees by area."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    vmt = schema.Object(
        title=_(u"VMT Map"),
        required=True,
        description=_(u"A vector map with the daily average VMT per household/employee per area."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
    scenario = schema.Object(
        title=_(u"LUC Scenario"),
        required=True,
        description=_(u"The LUC scenario that will provide spatialized inputs to the SCALDS model."),
        schema=Interface, # specify the interface(s) of the addable types here
    )
#
