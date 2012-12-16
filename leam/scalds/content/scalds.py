"""Definition of the SCALDS content type
"""
from xml.etree.ElementTree import Element, SubElement
from xml.etree.ElementTree import tostring

from zope.interface import implements

from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from archetypes.referencebrowserwidget import ReferenceBrowserWidget

# -*- Message Factory Imported Here -*-
from leam.scalds import scaldsMessageFactory as _

from leam.scalds.interfaces import ISCALDS
from leam.luc.interfaces import IModel
from leam.scalds.config import PROJECTNAME

SCALDSSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

    atapi.ReferenceField(
        'template',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"SCALDS Spreadsheet"),
            description=_(u"A SCALDS spreadsheet that will be used as a template."),
            startup_directory='/luc/impacts/scalds',
            allow_browse=True,
            allow_search=True,
        ),
        required=True,
        relationship='scalds_template',
        allowed_types=('File', 'Document'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'scenario',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"LUC Scenario"),
            description=_(u"The LUC scenario that will provide spatialized inputs to the SCALDS model."),
            startup_directory='/luc/scenarios',
        ),
        required=True,
        relationship='scalds_scenario',
        allowed_types=('LUC Scenario'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'vmt',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"VMT Map"),
            description=_(u"A vector map with the daily average VMT per household/employee per area."),
            startup_directory='/luc/impacts/scalds/vmt',
        ),
        required=True,
        relationship='scalds_vmt',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.ReferenceField(
        'water',
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u"Water and Sewer Costs"),
            description=_(u"A vector map providing costs associated with households/employees by area."),
            startup_directory='/luc/impacts/scalds/water',
        ),
        relationship='scalds_water',
        allowed_types=('SimMap'),
        multiValued=False,
    ),


    atapi.DateTimeField(
        'end_time',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Model End Time"),
            description=_(u"Logs when model ends execution."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        validators=('isValidDate'),
    ),


    atapi.DateTimeField(
        'start_time',
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u"Model Start Time"),
            description=_(u"Logs when the model begins execution."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        validators=('isValidDate'),
    ),


    atapi.StringField(
        'runstatus',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Model Run Status"),
            description=_(u"Maintain the state of the job."),
            visible={'view': 'hidden', 'edit': 'hidden'},
        ),
        required=True,
        default=_(u"queued"),
    ),

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

SCALDSSchema['title'].storage = atapi.AnnotationStorage()
SCALDSSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SCALDSSchema, moveDiscussion=False)


class SCALDS(base.ATCTContent):
    """Interface to the SCALDS Model."""
    implements(ISCALDS, IModel)

    meta_type = "SCALDS"
    schema = SCALDSSchema
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    template = atapi.ATReferenceFieldProperty('template')

    scenario = atapi.ATReferenceFieldProperty('scenario')

    vmt = atapi.ATReferenceFieldProperty('vmt')

    water = atapi.ATReferenceFieldProperty('water')

    end_time = atapi.ATFieldProperty('end_time')

    start_time = atapi.ATFieldProperty('start_time')

    runstatus = atapi.ATFieldProperty('runstatus')

    security.declarePublic('requeue')
    def requeue(self):
        """simple method to requeue the scenario"""
        self.runstatus = 'queued'
        self.reindexObject(['runstatus',])
        return "requeue"


    security.declarePublic('end_run')
    def end_run(self):
        """Mark the run as complete, set the end time, and set default
        page to summary.  

        NEEDS WORK -- should set the endtime field, should set the
        default page to the summary doc, should pass an arg that
        selects 'complete' or 'terminated'.
        """
        self.runstatus = 'complete'
        self.reindexObject(['runstatus',])

        #self.setDefaultPage(obj)
        return

    security.declarePublic('getConfig')
    def getConfig(self):
        """Returns the cconfiguration necessary for running the model"""
        #import pdb; pdb.set_trace()

        model = Element('model')
        tree = SubElement(model, 'scenario')
        SubElement(tree, 'id').text = self.id
        SubElement(tree, 'title').text = self.title
        SubElement(tree, 'repository').text = \
            'http://svn.leamgroup.com/desktop/ccrpc_scalds/trunk'
        SubElement(tree, 'cmdline').text = \
            'python startup -c config.xml'

        el = SubElement(tree, 'template')
        SubElement(el, 'title').text = self.getTemplate().title
        SubElement(el, 'download').text = self.getTemplate().absolute_url() + \
                '/at_download/file'

        el = SubElement(tree, 'scenario')
        SubElement(el, 'title').text = self.getScenario().title
        SubElement(el, 'url').text = self.getScenario().absolute_url()
        SubElement(el, 'config').text = self.getScenario().absolute_url() + \
                '/getConfig'

        el = SubElement(tree, 'vmt')
        SubElement(el, 'title').text = self.getVmt().title
        SubElement(el, 'download').text = self.getVmt().absolute_url() + \
                '/at_download/simImage'

        el = SubElement(tree, 'water')
        SubElement(el, 'title').text = self.getWater().title
        SubElement(el, 'download').text = self.getWater().absolute_url() + \
                '/at_download/simImage'

        self.REQUEST.RESPONSE.setHeader('Content-Type',
            'application/xml; charset=UTF-8')
        self.REQUEST.RESPONSE.setHeader('Content-Disposition',
            'attachment; filename="%s.xml"' % self.id)
        return tostring(model, encoding='UTF-8')


atapi.registerType(SCALDS, PROJECTNAME)
