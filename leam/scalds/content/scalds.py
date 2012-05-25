"""Definition of the SCALDS content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-
from leam.scalds import scaldsMessageFactory as _

from leam.scalds.interfaces import ISCALDS
from leam.scalds.config import PROJECTNAME

SCALDSSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.DateTimeField(
        'end_time',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Model End Time"),
            description=_(u"Logs when model ends execution."),
        ),
        validators=('isValidDate'),
    ),


    atapi.DateTimeField(
        'start_time',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Model Start Time"),
            description=_(u"Logs when the model begins execution."),
        ),
        validators=('isValidDate'),
    ),


    atapi.StringField(
        'runstatus',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Model Run Status"),
            description=_(u"Maintain the state of the job."),
        ),
        required=True,
        default=_(u"queued"),
    ),


    atapi.ReferenceField(
        'water',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ReferenceBrowserWidget(
            label=_(u"Water and Sewer Costs"),
            description=_(u"A vector map providing costs associated with households/employees by area."),
        ),
        relationship='scalds_water',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


    atapi.ReferenceField(
        'vmt',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ReferenceBrowserWidget(
            label=_(u"VMT Map"),
            description=_(u"A vector map with the daily average VMT per household/employee per area."),
        ),
        required=True,
        relationship='scalds_vmt',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


    atapi.ReferenceField(
        'scenario',
        storage=atapi.AnnotationStorage(),
        widget=atapi.ReferenceBrowserWidget(
            label=_(u"LUC Scenario"),
            description=_(u"The LUC scenario that will provide spatialized inputs to the SCALDS model."),
        ),
        required=True,
        relationship='scalds_scenario',
        allowed_types=(), # specify portal type names here ('Example Type',)
        multiValued=False,
    ),


))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

SCALDSSchema['title'].storage = atapi.AnnotationStorage()
SCALDSSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SCALDSSchema, moveDiscussion=False)


class SCALDS(base.ATCTContent):
    """Interface to the SCALDS Model."""
    implements(ISCALDS)

    meta_type = "SCALDS"
    schema = SCALDSSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    end_time = atapi.ATFieldProperty('end_time')

    start_time = atapi.ATFieldProperty('start_time')

    runstatus = atapi.ATFieldProperty('runstatus')

    water = atapi.ATReferenceFieldProperty('water')

    vmt = atapi.ATReferenceFieldProperty('vmt')

    scenario = atapi.ATReferenceFieldProperty('scenario')


atapi.registerType(SCALDS, PROJECTNAME)
