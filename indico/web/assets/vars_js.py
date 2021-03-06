from flask import render_template

from indico.modules.rb.models.locations import Location
from indico.web.flask.util import url_rule_to_js
from MaKaC.authentication.AuthenticationMgr import AuthenticatorMgr
from MaKaC.webinterface.common import tools as security_tools
from MaKaC.export import fileConverter
from MaKaC.webinterface import urlHandlers
from MaKaC.webinterface.materialFactories import MaterialFactoryRegistry


def generate_global_file(config):
    locations = Location.find_all() if config.getIsRoomBookingActive() else []
    location_names = {loc.name: loc.name for loc in locations}
    default_location = next((loc.name for loc in locations if loc.is_default), None)
    ext_auths = [(auth.id, auth.name) for auth in AuthenticatorMgr().getList() if auth.id != 'Local']
    file_type_icons = dict((k.lower(), v[2]) for k, v in config.getFileTypes().iteritems())
    material_types = dict((evt_type, [(m, m.title()) for m in MaterialFactoryRegistry._allowedMaterials[evt_type]])
                          for evt_type in ['meeting', 'simple_event', 'conference', 'category'])

    indico_vars = {
        'FileTypeIcons': file_type_icons,

        'Urls': {
            'ImagesBase': config.getImagesBaseURL(),
            'SecureImagesBase': config.getImagesBaseSecureURL(),

            'Login': urlHandlers.UHSignIn.getURL().js_router,
            'Favourites': urlHandlers.UHUserBaskets.getURL(_ignore_static=True).js_router,

            'ConferenceDisplay': urlHandlers.UHConferenceDisplay.getURL(_ignore_static=True).js_router,
            'ContributionDisplay': urlHandlers.UHContributionDisplay.getURL(_ignore_static=True).js_router,
            'SessionDisplay': urlHandlers.UHSessionDisplay.getURL(_ignore_static=True).js_router,

            'ContribToXML': urlHandlers.UHContribToXML.getURL(_ignore_static=True).js_router,
            'ContribToPDF': urlHandlers.UHContribToPDF.getURL(_ignore_static=True).js_router,

            'ConfTimeTablePDF': urlHandlers.UHConfTimeTablePDF.getURL(_ignore_static=True).js_router,
            'ConfTimeTableCustomPDF': urlHandlers.UHConfTimeTableCustomizePDF.getURL(_ignore_static=True).js_router,

            'SessionModification': urlHandlers.UHSessionModification.getURL(_ignore_static=True).js_router,
            'ContributionModification': urlHandlers.UHContributionModification.getURL(_ignore_static=True).js_router,
            'SessionProtection': urlHandlers.UHSessionModifAC.getURL(_ignore_static=True).js_router,
            'ContributionProtection': urlHandlers.UHContribModifAC.getURL(_ignore_static=True).js_router,

            'Reschedule': urlHandlers.UHConfModifReschedule.getURL(_ignore_static=True).js_router,
            'SlotCalc': urlHandlers.UHSessionModSlotCalc.getURL(_ignore_static=True).js_router,
            'FitSessionSlot': urlHandlers.UHSessionFitSlot.getURL(_ignore_static=True).js_router,

            'UploadAction': {
                'subcontribution': urlHandlers.UHSubContribModifAddMaterials.getURL(_ignore_static=True).js_router,
                'contribution': urlHandlers.UHContribModifAddMaterials.getURL(_ignore_static=True).js_router,
                'session': urlHandlers.UHSessionModifAddMaterials.getURL(_ignore_static=True).js_router,
                'conference': urlHandlers.UHConfModifAddMaterials.getURL(_ignore_static=True).js_router,
                'category': urlHandlers.UHCategoryAddMaterial.getURL(_ignore_static=True).js_router
            },

            'RoomBookingBookRoom': url_rule_to_js('rooms.room_book'),
            'RoomBookingBook': url_rule_to_js('rooms.book'),
            'RoomBookingDetails': urlHandlers.UHRoomBookingRoomDetails.getURL(_ignore_static=True).js_router,
            'RoomBookingCloneBooking': url_rule_to_js('rooms.roomBooking-cloneBooking'),
            'ConfModifSchedule': urlHandlers.UHConfModifSchedule.getURL(_ignore_static=True).js_router,
            'SubcontrModif': urlHandlers.UHContribModifSubCont.getURL(_ignore_static=True).js_router,
            'AuthorDisplay': urlHandlers.UHContribAuthorDisplay.getURL(_ignore_static=True).js_router,
            'AuthorEmail': urlHandlers.UHConferenceEmail.getURL(_ignore_static=True).js_router
        },

        'Data': {
            'MaterialTypes': material_types,
            'WeekDays': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
            'DefaultLocation': default_location,
            'Locations': location_names
        },

        'Security': {
            'allowedTags': ','.join(security_tools.allowedTags),
            'allowedAttributes': ','.join(security_tools.allowedAttrs),
            'allowedCssProperties': ','.join(security_tools.allowedCssProperties),
            'allowedProtocols': ','.join(security_tools.allowedProtocols),
            'urlProperties': ','.join(security_tools.urlProperties),
            'sanitizationLevel': config.getSanitizationLevel()
        },

        'Settings': {
            'ExtAuthenticators': ext_auths,
            'RoomBookingModuleActive': config.getIsRoomBookingActive()
        },

        'FileRestrictions': {
            'MaxUploadFilesTotalSize': config.getMaxUploadFilesTotalSize(),
            'MaxUploadFileSize': config.getMaxUploadFileSize()
        },

        'PDFConversion': {
            'AvailablePDFConversions': fileConverter.CDSConvFileConverter.getAvailableConversions(),
            'HasFileConverter': config.hasFileConverter()
        }
    }

    return render_template('assets/vars_globals.js', indico_vars=indico_vars, config=config, url_handlers=urlHandlers)
