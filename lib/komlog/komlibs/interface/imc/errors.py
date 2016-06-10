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

from enum import Enum

class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

# komlibs.interface.imc.api.events

    E_IIAE_USEREV_ECE       = 250000    #: proccess_message_USEREV. Error creating event

    E_IIAE_USEREVRESP_EPER  = 250100    #: proccess_message_USEREVRESP. Error processing event resp

# komlibs.interface.imc.api.gestconsole

    E_IIAG_MONVAR_EMV       = 251000    #: proccess_message_MONVAR. Error monitoring variable
    E_IIAG_MONVAR_BP        = 251001    #: proccess_message_MONVAR. Bad parameters

    E_IIAG_NEGVAR_EMNV      = 251100    #: proccess_message_NEGVAR. Error marking negative var
    E_IIAG_NEGVAR_BP        = 251101    #: proccess_message_NEGVAR. Bad parameters

    E_IIAG_POSVAR_EMPV      = 251200    #: proccess_message_POSVAR. Error marking positive var
    E_IIAG_POSVAR_BP        = 251201    #: proccess_message_POSVAR. Bad parameters

    E_IIAG_NEWUSR_ESWM      = 251300    #: proccess_message_NEWUSR. Error sending welcome mail
    E_IIAG_NEWUSR_BP        = 251301    #: proccess_message_NEWUSR. Bad parameters

    E_IIAG_NEWINV_ESIM      = 251400    #: proccess_message_NEWINV. Error sending invitation mail
    E_IIAG_NEWINV_BP        = 251401    #: proccess_message_NEWINV. Bad parameters

    E_IIAG_FORGETMAIL_ESIM  = 251500    #: proccess_message_FORGETMAIL. Error sending forget mail
    E_IIAG_FORGETMAIL_BP    = 251501    #: proccess_message_FORGETMAIL. Bad parameters

    E_IIAG_NEWDSW_ECW       = 251600    #: proccess_message_NEWDSW. Error creating widget
    E_IIAG_NEWDSW_BP        = 251601    #: proccess_message_NEWDSW. Bad parameters

    E_IIAG_NEWDPW_ECW       = 251700    #: proccess_message_NEWDPW. Error creating widget
    E_IIAG_NEWDPW_BP        = 251701    #: proccess_message_NEWDPW. Bad parameters

    E_IIAG_DELUSER_BP       = 251800    #: proccess_message_DELUSER. Bad parameters

    E_IIAG_DELAGENT_BP      = 251900    #: proccess_message_DELAGENT. Bad parameters

    E_IIAG_DELDS_BP         = 252000    #: proccess_message_DELDS. Bad parameters

    E_IIAG_DELDP_BP         = 252100    #: proccess_message_DELDP. Bad parameters

    E_IIAG_DELWIDGET_BP     = 252200    #: proccess_message_DELWIDGET. Bad parameters

    E_IIAG_DELDASHB_BP      = 252300    #: proccess_message_DELDASHB. Bad parameters

# komlibs.interface.imc.api.rescontrol

    E_IIARC_UPDQUO_EUQ      = 253000    #: proccess_message_UPDQUO. error updating quotes

    E_IIARC_RESAUTH_EUR     = 253100    #: proccess_message_RESAUTH. error updating resources

# komlibs.interface.imc.api.storing

    E_IIAST_STOSMP_ERF      = 254000    #: proccess_message_STOSMP. error in initial rename
    E_IIAST_STOSMP_ERFALC   = 254001    #: proccess_message_STOSMP. error renaming after failed load
    E_IIAST_STOSMP_ELFC     = 254002    #: proccess_message_STOSMP. error loading content
    E_IIAST_STOSMP_ERFALC2  = 254003    #: proccess_message_STOSMP. error renaming after failed load
    E_IIAST_STOSMP_ELJC     = 254004    #: proccess_message_STOSMP. error loading json content
    E_IIAST_STOSMP_ERFACC   = 254005    #: proccess_message_STOSMP. error renaming after check fail 
    E_IIAST_STOSMP_ECC      = 254006    #: proccess_message_STOSMP. error checking content
    E_IIAST_STOSMP_ERFAFP   = 254007    #: proccess_message_STOSMP. error renaming after fail proc 
    E_IIAST_STOSMP_ESDSD    = 254008    #: proccess_message_STOSMP. error storing ds data

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



# komlibs.interface.imc.model.messages

    E_IIMM_SSM_ISF          = 260000    #: StoreSampleMessage. invalid sample file

    E_IIMM_MVM_IDID         = 260100    #: MapVarsMessage. invalid did
    E_IIMM_MVM_IDT          = 260101    #: MapVarsMessage. invalid date

    E_IIMM_MONVAR_IUID      = 260200    #: MonitorVariableMessage. invalid uid
    E_IIMM_MONVAR_IDID      = 260201    #: MonitorVariableMessage. invalid did
    E_IIMM_MONVAR_IDT       = 260202    #: MonitorVariableMessage. invalid date
    E_IIMM_MONVAR_IPOS      = 260203    #: MonitorVariableMessage. invalid position
    E_IIMM_MONVAR_ILEN      = 260204    #: MonitorVariableMessage. invalid length
    E_IIMM_MONVAR_IDPN      = 260205    #: MonitorVariableMessage. invalid datapoint name

    E_IIMM_GDTREE_IPID      = 260300    #: GenerateDTreeMessage. invalid pid

    E_IIMM_FILLDP_IPID      = 260400    #: FillDatapointMessage. invalid pid
    E_IIMM_FILLDP_IDT       = 260401    #: FillDatapointMessage. invalid date

    E_IIMM_FILLDS_IDID      = 260500    #: FillDatasourceMessage. invalid did
    E_IIMM_FILLDS_IDT       = 260501    #: FillDatasourceMessage. invalid date

    E_IIMM_NEGVAR_IPID      = 260600    #: NegativeVariableMessage. invalid pid
    E_IIMM_NEGVAR_IDT       = 260601    #: NegativeVariableMessage. invalid date
    E_IIMM_NEGVAR_IPOS      = 260602    #: NegativeVariableMessage. invalid position
    E_IIMM_NEGVAR_ILEN      = 260603    #: NegativeVariableMessage. invalid length

    E_IIMM_POSVAR_IPID      = 260700    #: PositiveVariableMessage. invalid pid
    E_IIMM_POSVAR_IDT       = 260701    #: PositiveVariableMessage. invalid date
    E_IIMM_POSVAR_IPOS      = 260702    #: PositiveVariableMessage. invalid position
    E_IIMM_POSVAR_ILEN      = 260703    #: PositiveVariableMessage. invalid lenght

    E_IIMM_NEWUSR_IEMAIL    = 260800    #: NewUserNotificationMessage. invalid email
    E_IIMM_NEWUSR_ICODE     = 260801    #: NewUserNotificationMessage. invalid code

    E_IIMM_UPDQUO_IPRM      = 260900    #: UpdateQuotesMessage. invalid params
    E_IIMM_UPDQUO_IOP       = 260901    #: UpdateQuotesMessage. invalid operation

    E_IIMM_RESAUTH_IPRM     = 261000    #: ResourceAuthorizationUpdateMessage. invalid params
    E_IIMM_RESAUTH_IOP      = 261001    #: ResourceAuthorizationUpdateMessage. invalid operation

    E_IIMM_NEWDPW_IUID      = 261100    #: NewDPWidgetMessage. invalid uid
    E_IIMM_NEWDPW_IPID      = 261101    #: NewDPWidgetMessage. invalid pid

    E_IIMM_NEWDSW_IUID      = 261150    #: NewDSWidgetMessage. invalid uid
    E_IIMM_NEWDSW_IDID      = 261151    #: NewDSWidgetMessage. invalid did

    E_IIMM_DELUSER_IUID     = 261200    #: DeleteUserMessage. invalid uid

    E_IIMM_DELAGENT_IAID    = 261300    #: DeleteAgentMessage. invalid aid

    E_IIMM_DELDS_IDID       = 261400    #: DeleteDatasourceMessage. invalid did

    E_IIMM_DELDP_IPID       = 261500    #: DeleteDatapointMessage. invalid pid

    E_IIMM_DELWIDGET_IWID   = 261600    #: DeleteWidgetMessage. invalid wid

    E_IIMM_DELDASHB_IBID    = 261700    #: DeleteDashboardMessage. invalid bid

    E_IIMM_USEREV_IUID      = 261800    #: UserEventMessage. invalid uid
    E_IIMM_USEREV_IET       = 261801    #: UserEventMessage. invalid event type
    E_IIMM_USEREV_IPRM      = 261802    #: UserEventMessage. invalid params

    E_IIMM_USEREVR_IUID     = 261900    #: UserEventResponseMessage. invalid uid
    E_IIMM_USEREVR_IDT      = 261901    #: UserEventResponseMessage. invalid date
    E_IIMM_USEREVR_IPRM     = 261902    #: UserEventResponseMessage. invalid params

    E_IIMM_GTXS_IDID        = 262000     #: GenerateTextSummaryMessage. invalid did
    E_IIMM_GTXS_IDT         = 262001     #: GenerateTextSummaryMessage. invalid date

    E_IIMM_MISSDP_IDID      = 262100     #: MissingDatapointMessage. invalid did
    E_IIMM_MISSDP_IDT       = 262101     #: MissingDatapointMessage. invalid date

    E_IIMM_NEWINV_IEMAIL    = 262200     #: NewInvitationMailMessage. invalid email
    E_IIMM_NEWINV_IINV      = 262201     #: NewInvitationMailMessage. invalid invitation id

    E_IIMM_FORGET_IEMAIL    = 262300     #: ForgetMailMailMessage. invalid email
    E_IIMM_FORGET_ICODE     = 262301     #: ForgetMailMailMessage. invalid code

