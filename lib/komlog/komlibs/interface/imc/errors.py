'''
In this file we define the different error codes that will be
added to the exceptions in the interface web modules, to identify
the point in the code where it raised

The pattern used to name an error is:

E_XXX_YYY_ZZZ

where:

- XXX is the code to identify the file
- YYY is the code to identify the function
- ZZZ is the code to identify the reason the exception was raised

The range reserved for Errors.in this module is 250000 - 300000

'''

from enum import Enum, unique

@unique
class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

# komlibs.interface.imc.api.events

    E_IIAE_USEREV_ECE       = 250000    #: proccess_message_USEREV. Error creating event

    E_IIAE_USEREVRESP_EPER  = 250100    #: proccess_message_USEREVRESP. Error processing event resp

# komlibs.interface.imc.api.gestconsole

    E_IIAG_MONVAR_EMV       = 251000    #: proccess_message_MONVAR. Error monitoring variable

    E_IIAG_NEGVAR_EMNV      = 251100    #: proccess_message_NEGVAR. Error marking negative var

    E_IIAG_POSVAR_EMPV      = 251200    #: proccess_message_POSVAR. Error marking positive var

    E_IIAG_NEWUSR_ESWM      = 251300    #: proccess_message_NEWUSR. Error sending welcome mail

    E_IIAG_NEWINV_ESIM      = 251400    #: proccess_message_NEWINV. Error sending invitation mail

    E_IIAG_FORGETMAIL_ESFM  = 251500    #: proccess_message_FORGETMAIL. Error sending forget mail

    E_IIAG_NEWDSW_ECW       = 251600    #: proccess_message_NEWDSW. Error creating widget

    E_IIAG_NEWDPW_ECW       = 251700    #: proccess_message_NEWDPW. Error creating widget

# komlibs.interface.imc.api.rescontrol

    E_IIARC_UPDQUO_EUQ      = 253000    #: proccess_message_UPDQUO. error updating quotes

    E_IIARC_RESAUTH_EUR     = 253100    #: proccess_message_RESAUTH. error updating resources

# komlibs.interface.imc.api.storing (deprecated 254000 - 254999 free)

# komlibs.interface.imc.api.textmining

    E_IIATM_GDTREE_IP       = 255000    #: proccess_message_GDTREE. invalid pid
    E_IIATM_GDTREE_EGDT     = 255001    #: proccess_message_GDTREE. error generating decision tree

    E_IIATM_MAPVARS_IDID    = 255100    #: proccess_message_MAPVARS. invalid did
    E_IIATM_MAPVARS_IDT     = 255101    #: proccess_message_MAPVARS. invalid date
    E_IIATM_MAPVARS_EGDSM   = 255102    #: proccess_message_MAPVARS. error generating ds map

    E_IIATM_FILLDP_IPID     = 255200    #: proccess_message_FILLDP. invalid pid
    E_IIATM_FILLDP_IDT      = 255201    #: proccess_message_FILLDP. invalid date
    E_IIATM_FILLDP_ESDPV    = 255202    #: proccess_message_FILLDP. error storing datapoint values

    E_IIATM_FILLDS_IDID     = 255300    #: proccess_message_FILLDS. invalid did
    E_IIATM_FILLDS_IDT      = 255301    #: proccess_message_FILLDS. invalid date
    E_IIATM_FILLDS_ESDSV    = 255302    #: proccess_message_FILLDS. error storing datasource values

    E_IIATM_GTXS_IDID       = 255400    #: proccess_message_GENTEXTSUMMARY. invalid did
    E_IIATM_GTXS_IDT        = 255401    #: proccess_message_GENTEXTSUMMARY. invalid date
    E_IIATM_GTXS_EGDSTXS    = 255402    #: proccess_message_GENTEXTSUMMARY. error gen ds text summ


# komlibs.interface.imc.api.lambdas

    E_IIALD_SSDT_MRE        = 256000    #: process_message_SSDATA. message routing error
    E_IIALD_SSDT_SUS        = 256001    #: process_message_SSDATA. session unset successfully
    E_IIALD_SSDT_SUE        = 256002    #: process_message_SSDATA. session unset error
    E_IIALD_SSDT_SNF        = 256003    #: process_message_SSDATA. session not found

    E_IIALD_DATINT_NSA      = 256100    #: process_message_DATINT. session address not set
    E_IIALD_DATINT_SEXP     = 256101    #: process_message_DATINT. session expired

# komlibs.interface.imc.model.messages

    E_IIMM_IMC_UMT          = 260050    #: IMCMessage. Unknown message type
    E_IIMM_IMC_MNS          = 260051    #: IMCMessage. message not supported

    E_IIMM_MVM_IDID         = 260100    #: MapVarsMessage. invalid did
    E_IIMM_MVM_IDT          = 260101    #: MapVarsMessage. invalid date
    E_IIMM_MVM_ELFS         = 260102    #: MapVarsMessage. error loading from string
    E_IIMM_MVM_MINS         = 260103    #: MapVarsMessage. msg is not string
    E_IIMM_MVM_IST          = 260104    #: MapVarsMessage. invalid serialization type
    E_IIMM_MVM_IHDID        = 260105    #: MapVarsMessage. invalid hex did
    E_IIMM_MVM_IHDATE       = 260106    #: MapVarsMessage. invalid hex date

    E_IIMM_MONVAR_IUID      = 260200    #: MonitorVariableMessage. invalid uid
    E_IIMM_MONVAR_IDID      = 260201    #: MonitorVariableMessage. invalid did
    E_IIMM_MONVAR_IDT       = 260202    #: MonitorVariableMessage. invalid date
    E_IIMM_MONVAR_IPOS      = 260203    #: MonitorVariableMessage. invalid position
    E_IIMM_MONVAR_ILEN      = 260204    #: MonitorVariableMessage. invalid length
    E_IIMM_MONVAR_IDPN      = 260205    #: MonitorVariableMessage. invalid datapoint name
    E_IIMM_MONVAR_ELFS      = 260206    #: MonitorVariableMessage. error loading from string
    E_IIMM_MONVAR_MINS      = 260207    #: MonitorVariableMessage. msg is not string
    E_IIMM_MONVAR_IST       = 260208    #: MonitorVariableMessage. invalid serialization type
    E_IIMM_MONVAR_IHUID     = 260209    #: MonitorVariableMessage. invalid hex uid
    E_IIMM_MONVAR_IHDID     = 260210    #: MonitorVariableMessage. invalid hex did
    E_IIMM_MONVAR_IHDATE    = 260211    #: MonitorVariableMessage. invalid hex date
    E_IIMM_MONVAR_ISPOS     = 260212    #: MonitorVariableMessage. invalid string position
    E_IIMM_MONVAR_ISLEN     = 260213    #: MonitorVariableMessage. invalid string length

    E_IIMM_GDTREE_IPID      = 260300    #: GenerateDTreeMessage. invalid pid
    E_IIMM_GDTREE_ELFS      = 260301    #: GenerateDTreeMessage. error loading from string
    E_IIMM_GDTREE_MINS      = 260302    #: GenerateDTreeMessage. msg is not string
    E_IIMM_GDTREE_IST       = 260303    #: GenerateDTreeMessage. invalid serialization type
    E_IIMM_GDTREE_IHPID     = 260304    #: GenerateDTreeMessage. invalid hex pid

    E_IIMM_FILLDP_IPID      = 260400    #: FillDatapointMessage. invalid pid
    E_IIMM_FILLDP_IDT       = 260401    #: FillDatapointMessage. invalid date
    E_IIMM_FILLDP_ELFS      = 260402    #: FillDatapointMessage. error loading from string
    E_IIMM_FILLDP_MINS      = 260403    #: FillDatapointMessage. msg is not string
    E_IIMM_FILLDP_IST       = 260404    #: FillDatapointMessage. invalid serialization type
    E_IIMM_FILLDP_IHPID     = 260405    #: FillDatapointMessage. invalid hex pid
    E_IIMM_FILLDP_IHDATE    = 260406    #: FillDatapointMessage. invalid hex date

    E_IIMM_FILLDS_IDID      = 260500    #: FillDatasourceMessage. invalid did
    E_IIMM_FILLDS_IDT       = 260501    #: FillDatasourceMessage. invalid date
    E_IIMM_FILLDS_ELFS      = 260502    #: FillDatasourceMessage. error loading from string
    E_IIMM_FILLDS_MINS      = 260503    #: FillDatasourceMessage. msg is not string
    E_IIMM_FILLDS_IST       = 260504    #: FillDatasourceMessage. invalid serialization type
    E_IIMM_FILLDS_IHDID     = 260505    #: FillDatasourceMessage. invalid hex did
    E_IIMM_FILLDS_IHDATE    = 260506    #: FillDatasourceMessage. invalid hex date

    E_IIMM_NEGVAR_IPID      = 260600    #: NegativeVariableMessage. invalid pid
    E_IIMM_NEGVAR_IDT       = 260601    #: NegativeVariableMessage. invalid date
    E_IIMM_NEGVAR_IPOS      = 260602    #: NegativeVariableMessage. invalid position
    E_IIMM_NEGVAR_ILEN      = 260603    #: NegativeVariableMessage. invalid length
    E_IIMM_NEGVAR_ELFS      = 260604    #: NegativeVariableMessage. error loading from string
    E_IIMM_NEGVAR_MINS      = 260605    #: NegativeVariableMessage. msg is not string
    E_IIMM_NEGVAR_IST       = 260606    #: NegativeVariableMessage. invalid serialization type
    E_IIMM_NEGVAR_IHPID     = 260607    #: NegativeVariableMessage. invalid hex pid
    E_IIMM_NEGVAR_IHDATE    = 260608    #: NegativeVariableMessage. invalid hex date
    E_IIMM_NEGVAR_ISPOS     = 260609    #: NegativeVariableMessage. invalid string position
    E_IIMM_NEGVAR_ISLEN     = 260610    #: NegativeVariableMessage. invalid string length

    E_IIMM_POSVAR_IPID      = 260700    #: PositiveVariableMessage. invalid pid
    E_IIMM_POSVAR_IDT       = 260701    #: PositiveVariableMessage. invalid date
    E_IIMM_POSVAR_IPOS      = 260702    #: PositiveVariableMessage. invalid position
    E_IIMM_POSVAR_ILEN      = 260703    #: PositiveVariableMessage. invalid lenght
    E_IIMM_POSVAR_ELFS      = 260704    #: PositiveVariableMessage. error loading from string
    E_IIMM_POSVAR_MINS      = 260705    #: PositiveVariableMessage. msg is not string
    E_IIMM_POSVAR_IST       = 260706    #: PositiveVariableMessage. invalid serialization type
    E_IIMM_POSVAR_IHPID     = 260707    #: PositiveVariableMessage. invalid hex pid
    E_IIMM_POSVAR_IHDATE    = 260708    #: PositiveVariableMessage. invalid hex date
    E_IIMM_POSVAR_ISPOS     = 260709    #: PositiveVariableMessage. invalid string position
    E_IIMM_POSVAR_ISLEN     = 260710    #: PositiveVariableMessage. invalid string length

    E_IIMM_NEWUSR_IEMAIL    = 260800    #: NewUserNotificationMessage. invalid email
    E_IIMM_NEWUSR_ICODE     = 260801    #: NewUserNotificationMessage. invalid code
    E_IIMM_NEWUSR_ELFS      = 260802    #: NewUserNotificationMessage. error loading from string
    E_IIMM_NEWUSR_MINS      = 260803    #: NewUserNotificationMessage. msg is not string
    E_IIMM_NEWUSR_IST       = 260804    #: NewUserNotificationMessage. invalid serialization type

    E_IIMM_UPDQUO_IPRM      = 260900    #: UpdateQuotesMessage. invalid params
    E_IIMM_UPDQUO_IOP       = 260901    #: UpdateQuotesMessage. invalid operation
    E_IIMM_UPDQUO_ELFS      = 260902    #: UpdateQuotesMessage. error loading from string
    E_IIMM_UPDQUO_MINS      = 260903    #: UpdateQuotesMessage. msg is not string
    E_IIMM_UPDQUO_IST       = 260904    #: UpdateQuotesMessage. invalid serialization type
    E_IIMM_UPDQUO_IJSPRM    = 260905    #: UpdateQuotesMessage. invalid json parameters
    E_IIMM_UPDQUO_IOPN      = 260906    #: UpdateQuotesMessage. invalid operation name

    E_IIMM_RESAUTH_IPRM     = 261000    #: ResourceAuthorizationUpdateMessage. invalid params
    E_IIMM_RESAUTH_IOP      = 261001    #: ResourceAuthorizationUpdateMessage. invalid operation
    E_IIMM_RESAUTH_ELFS     = 261002    #: ResourceAuthorizationUpdateMessage. error loading from str
    E_IIMM_RESAUTH_MINS     = 261003    #: ResourceAuthorizationUpdateMessage. msg is not string
    E_IIMM_RESAUTH_IST      = 261004    #: ResourceAuthorizationUpdateMessage. inv serialization type
    E_IIMM_RESAUTH_IJSPRM   = 261005    #: ResourceAuthorizationUpdateMessage. inv json parameters
    E_IIMM_RESAUTH_IOPN     = 261006    #: ResourceAuthorizationUpdateMessage. invalid operation name

    E_IIMM_NEWDPW_IUID      = 261100    #: NewDPWidgetMessage. invalid uid
    E_IIMM_NEWDPW_IPID      = 261101    #: NewDPWidgetMessage. invalid pid
    E_IIMM_NEWDPW_ELFS      = 261102    #: NewDPWidgetMessage. error loading from string
    E_IIMM_NEWDPW_MINS      = 261103    #: NewDPWidgetMessage. msg is not string
    E_IIMM_NEWDPW_IST       = 261104    #: NewDPWidgetMessage. invalid serialization type
    E_IIMM_NEWDPW_IHUID     = 261105    #: NewDPWidgetMessage. invalid hex uid
    E_IIMM_NEWDPW_IHPID     = 261106    #: NewDPWidgetMessage. invalid hex pid

    E_IIMM_NEWDSW_IUID      = 261150    #: NewDSWidgetMessage. invalid uid
    E_IIMM_NEWDSW_IDID      = 261151    #: NewDSWidgetMessage. invalid did
    E_IIMM_NEWDSW_ELFS      = 261152    #: NewDSWidgetMessage. error loading from string
    E_IIMM_NEWDSW_MINS      = 261153    #: NewDSWidgetMessage. msg is not string
    E_IIMM_NEWDSW_IST       = 261154    #: NewDSWidgetMessage. invalid serialization type
    E_IIMM_NEWDSW_IHUID     = 261155    #: NewDSWidgetMessage. invalid hex uid
    E_IIMM_NEWDSW_IHDID     = 261156    #: NewDSWidgetMessage. invalid hex did

    E_IIMM_DELUSER_IUID     = 261200    #: DeleteUserMessage. invalid uid
    E_IIMM_DELUSER_ELFS     = 261201    #: DeleteUserMessage. error loading from string
    E_IIMM_DELUSER_MINS     = 261202    #: DeleteUserMessage. msg is not string
    E_IIMM_DELUSER_IST      = 261203    #: DeleteUserMessage. invalid serialization type
    E_IIMM_DELUSER_IHUID    = 261204    #: DeleteUserMessage. invalid hex uid

    E_IIMM_DELAGENT_IAID    = 261300    #: DeleteAgentMessage. invalid aid
    E_IIMM_DELAGENT_ELFS    = 261301    #: DeleteAgentMessage. error loading from string
    E_IIMM_DELAGENT_MINS    = 261302    #: DeleteAgentMessage. msg is not string
    E_IIMM_DELAGENT_IST     = 261303    #: DeleteAgentMessage. invalid serialization type
    E_IIMM_DELAGENT_IHAID   = 261304    #: DeleteAgentMessage. invalid hex aid

    E_IIMM_DELDS_IDID       = 261400    #: DeleteDatasourceMessage. invalid did
    E_IIMM_DELDS_ELFS       = 261401    #: DeleteDatasourceMessage. error loading from string
    E_IIMM_DELDS_MINS       = 261402    #: DeleteDatasourceMessage. msg is not string
    E_IIMM_DELDS_IST        = 261403    #: DeleteDatasourceMessage. invalid serialization type
    E_IIMM_DELDS_IHDID      = 261404    #: DeleteDatasourceMessage. invalid hex did

    E_IIMM_DELDP_IPID       = 261500    #: DeleteDatapointMessage. invalid pid
    E_IIMM_DELDP_ELFS       = 261501    #: DeleteDatapointMessage. error loading from string
    E_IIMM_DELDP_MINS       = 261502    #: DeleteDatapointMessage. msg is not string
    E_IIMM_DELDP_IST        = 261503    #: DeleteDatapointMessage. invalid serialization type
    E_IIMM_DELDP_IHPID      = 261504    #: DeleteDatapointMessage. invalid hex pid

    E_IIMM_DELWIDGET_IWID   = 261600    #: DeleteWidgetMessage. invalid wid
    E_IIMM_DELWIDGET_ELFS   = 261601    #: DeleteWidgetMessage. error loading from string
    E_IIMM_DELWIDGET_MINS   = 261602    #: DeleteWidgetMessage. msg is not string
    E_IIMM_DELWIDGET_IST    = 261603    #: DeleteWidgetMessage. invalid serialization type
    E_IIMM_DELWIDGET_IHWID  = 261604    #: DeleteWidgetMessage. invalid hex wid

    E_IIMM_DELDASHB_IBID    = 261700    #: DeleteDashboardMessage. invalid bid
    E_IIMM_DELDASHB_ELFS    = 261701    #: DeleteDashboardMessage. error loading from string
    E_IIMM_DELDASHB_MINS    = 261702    #: DeleteDashboardMessage. msg is not string
    E_IIMM_DELDASHB_IST     = 261703    #: DeleteDashboardMessage. invalid serialization type
    E_IIMM_DELDASHB_IHBID   = 261704    #: DeleteDashboardMessage. invalid hex bid

    E_IIMM_USEREV_IUID      = 261800    #: UserEventMessage. invalid uid
    E_IIMM_USEREV_IET       = 261801    #: UserEventMessage. invalid event type
    E_IIMM_USEREV_IPRM      = 261802    #: UserEventMessage. invalid params
    E_IIMM_USEREV_ELFS      = 261803    #: UserEventMessage. error loading from string
    E_IIMM_USEREV_MINS      = 261804    #: UserEventMessage. msg is not string
    E_IIMM_USEREV_IST       = 261805    #: UserEventMessage. invalid serialization type
    E_IIMM_USEREV_IHUID     = 261806    #: UserEventMessage. invalid hex uid
    E_IIMM_USEREV_ISET      = 261807    #: UserEventMessage. invalid string event type
    E_IIMM_USEREV_IJSPRM    = 261808    #: UserEventMessage. invalid json parameters

    E_IIMM_USEREVR_IUID     = 261900    #: UserEventResponseMessage. invalid uid
    E_IIMM_USEREVR_IDT      = 261901    #: UserEventResponseMessage. invalid date
    E_IIMM_USEREVR_IPRM     = 261902    #: UserEventResponseMessage. invalid params
    E_IIMM_USEREVR_ELFS     = 261903    #: UserEventResponseMessage. error loading from string
    E_IIMM_USEREVR_MINS     = 261904    #: UserEventResponseMessage. msg is not string
    E_IIMM_USEREVR_IST      = 261905    #: UserEventResponseMessage. invalid serialization type
    E_IIMM_USEREVR_IHUID    = 261906    #: UserEventResponseMessage. invalid hex uid
    E_IIMM_USEREVR_IHDATE   = 261907    #: UserEventResponseMessage. invalid hex date
    E_IIMM_USEREVR_IJSPRM   = 261908    #: UserEventResponseMessage. invalid json parameters

    E_IIMM_GTXS_IDID        = 262000    #: GenerateTextSummaryMessage. invalid did
    E_IIMM_GTXS_IDT         = 262001    #: GenerateTextSummaryMessage. invalid date
    E_IIMM_GTXS_ELFS        = 262002    #: GenerateTextSummaryMessage. error loading from string
    E_IIMM_GTXS_MINS        = 262003    #: GenerateTextSummaryMessage. msg is not string
    E_IIMM_GTXS_IST         = 262004    #: GenerateTextSummaryMessage. invalid serialization type
    E_IIMM_GTXS_IHDID       = 262005    #: GenerateTextSummaryMessage. invalid hex did
    E_IIMM_GTXS_IHDATE      = 262006    #: GenerateTextSummaryMessage. invalid hex date

    E_IIMM_MISSDP_IDID      = 262100    #: MissingDatapointMessage. invalid did
    E_IIMM_MISSDP_IDT       = 262101    #: MissingDatapointMessage. invalid date
    E_IIMM_MISSDP_ELFS      = 262102    #: MissingDatapointMessage. error loading from string
    E_IIMM_MISSDP_MINS      = 262103    #: MissingDatapointMessage. msg is not string
    E_IIMM_MISSDP_IST       = 262104    #: MissingDatapointMessage. invalid serialization type
    E_IIMM_MISSDP_IHDID     = 262105    #: MissingDatapointMessage. invalid hex did
    E_IIMM_MISSDP_IHDATE    = 262106    #: MissingDatapointMessage. invalid hex date

    E_IIMM_NEWINV_IEMAIL    = 262200    #: NewInvitationMailMessage. invalid email
    E_IIMM_NEWINV_IINV      = 262201    #: NewInvitationMailMessage. invalid invitation id
    E_IIMM_NEWINV_ELFS      = 262202    #: NewInvitationMailMessage. error loading from string
    E_IIMM_NEWINV_MINS      = 262203    #: NewInvitationMailMessage. msg is not string
    E_IIMM_NEWINV_IST       = 262204    #: NewInvitationMailMessage. invalid serialization type
    E_IIMM_NEWINV_IHINV     = 262205    #: NewInvitationMailMessage. invalid hex inv

    E_IIMM_FORGET_IEMAIL    = 262300    #: ForgetMailMessage. invalid email
    E_IIMM_FORGET_ICODE     = 262301    #: ForgetMailMessage. invalid code
    E_IIMM_FORGET_ELFS      = 262302    #: ForgetMailMessage. error loading from string
    E_IIMM_FORGET_MINS      = 262303    #: ForgetMailMessage. msg is not string
    E_IIMM_FORGET_IST       = 262304    #: ForgetMailMessage. invalid serialization type
    E_IIMM_FORGET_IHCODE    = 262305    #: ForgetMailMessage. invalid hex code

    E_IIMM_URUP_IDT         = 262400    #: UrisUpdatedMessage. Invalid date
    E_IIMM_URUP_IURIS       = 262401    #: UrisUpdatedMessage. Invalid uris
    E_IIMM_URUP_ELFS        = 262402    #: UrisUpdatedMessage. error loading from string
    E_IIMM_URUP_MINS        = 262403    #: UrisUpdatedMessage. msg is not string
    E_IIMM_URUP_IST         = 262404    #: UrisUpdatedMessage. invalid serialization type
    E_IIMM_URUP_IHDATE      = 262405    #: UrisUpdatedMessage. invalid hex date
    E_IIMM_URUP_IJSURIS     = 262406    #: UrisUpdatedMessage. invalid json uris

    E_IIMM_SSDT_ISID        = 262500    #: SendSessionDataMessage. Invalid sid
    E_IIMM_SSDT_ELFS        = 262501    #: SendSessionDataMessage. error loading from string
    E_IIMM_SSDT_MINS        = 262502    #: SendSessionDataMessage. msg is not string
    E_IIMM_SSDT_IST         = 262503    #: SendSessionDataMessage. invalid serialization type
    E_IIMM_SSDT_IHSID       = 262504    #: SendSessionDataMessage. invalid hex date
    E_IIMM_SSDT_IJSDATA     = 262505    #: SendSessionDataMessage. invalid json data

    E_IIMM_CSH_ISID         = 262600    #: ClearSessionHooksMessage. Invalid sid
    E_IIMM_CSH_IIDS         = 262601    #: ClearSessionHooksMessage. Invalid ids
    E_IIMM_CSH_ELFS         = 262602    #: ClearSessionHooksMessage. error loading from string
    E_IIMM_CSH_MINS         = 262603    #: ClearSessionHooksMessage. msg is not string
    E_IIMM_CSH_IST          = 262604    #: ClearSessionHooksMessage. invalid serialization type
    E_IIMM_CSH_IHSID        = 262605    #: ClearSessionHooksMessage. invalid hex sid
    E_IIMM_CSH_IJSIDS       = 262606    #: ClearSessionHooksMessage. invalid json ids

    E_IIMM_HNU_IUID         = 262700    #: HookNewUrisMessage. invalid uid
    E_IIMM_HNU_IDT          = 262701    #: HookNewUrisMessage. invalid date
    E_IIMM_HNU_IURIS        = 262702    #: HookNewUrisMessage. invalid uris
    E_IIMM_HNU_ELFS         = 262703    #: HookNewUrisMessage. error loading from string
    E_IIMM_HNU_MINS         = 262704    #: HookNewUrisMessage. msg is not string
    E_IIMM_HNU_IST          = 262705    #: HookNewUrisMessage. invalid serialization type
    E_IIMM_HNU_IHUID        = 262706    #: HookNewUrisMessage. invalid hex uid
    E_IIMM_HNU_IHDATE       = 262707    #: HookNewUrisMessage. invalid hex date
    E_IIMM_HNU_IJSURIS      = 262708    #: HookNewUrisMessage. invalid json uris

    E_IIMM_DIRM_ISID        = 262800    #: DataIntervalRequestMessage. invalid sid
    E_IIMM_DIRM_III         = 262801    #: DataIntervalRequestMessage. invalid interval init
    E_IIMM_DIRM_IIE         = 262802    #: DataIntervalRequestMessage. invalid interval end
    E_IIMM_DIRM_IURI        = 262803    #: DataIntervalRequestMessage. invalid uri
    E_IIMM_DIRM_ELFS        = 262804    #: DataIntervalRequestMessage. error loading from string
    E_IIMM_DIRM_MINS        = 262805    #: DataIntervalRequestMessage. msg is not string
    E_IIMM_DIRM_IST         = 262806    #: DataIntervalRequestMessage. invalid serialization type
    E_IIMM_DIRM_IHSID       = 262807    #: DataIntervalRequestMessage. invalid hex sid
    E_IIMM_DIRM_IHII        = 262808    #: DataIntervalRequestMessage. invalid hex interval init
    E_IIMM_DIRM_IHIE        = 262809    #: DataIntervalRequestMessage. invalid hex interval end
    E_IIMM_DIRM_IJSURI      = 262810    #: DataIntervalRequestMessage. invalid json uri
    E_IIMM_DIRM_ICOUNT      = 262811    #: DataIntervalRequestMessage. invalid count
    E_IIMM_DIRM_IJSCOUNT    = 262812    #: DataIntervalRequestMessage. invalid json count
    E_IIMM_DIRM_IIRT        = 262813    #: DataIntervalRequestMessage. invalid irt
    E_IIMM_DIRM_IJSIRT      = 262814    #: DataIntervalRequestMessage. invalid json irt

    E_IIMM_ADTREE_IPID      = 262900    #: AnalyzeDTreeMessage. invalid pid
    E_IIMM_ADTREE_ELFS      = 262901    #: AnalyzeDTreeMessage. error loading from string
    E_IIMM_ADTREE_MINS      = 262902    #: AnalyzeDTreeMessage. msg is not string
    E_IIMM_ADTREE_IST       = 262903    #: AnalyzeDTreeMessage. invalid serialization type
    E_IIMM_ADTREE_IHPID     = 262904    #: AnalyzeDTreeMessage. invalid hex pid

    E_IIMM_IDNEWDPS_IDID    = 262950    #: IdentifyNewDatapoints. invalid did
    E_IIMM_IDNEWDPS_ELFS    = 262951    #: IdentifyNewDatapoints. error loading from string
    E_IIMM_IDNEWDPS_MINS    = 262952    #: IdentifyNewDatapoints. msg is not string
    E_IIMM_IDNEWDPS_IST     = 262953    #: IdentifyNewDatapoints. invalid serialization type
    E_IIMM_IDNEWDPS_IHDID   = 262954    #: IdentifyNewDatapoints. invalid hex did

