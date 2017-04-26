/**
 * Created by lujian on 2017-04-25.
 */


function onClickBtn(o,data_package){
    this.id = o.id;
    alert(this.id);
}
function staticTable1View(table_id, table_data) {
    var tbHTML='';
    var tbButtonID = [];
    for (var i = 0; i < table_data.length; i++) {
        var td_i = '';
        td_i= (function (i) {
            this.td = '';
            this.TableMake = function () {
                if (i ===0){
                    this.td= [
                        '<tr>',
                        '<td>', (i+1), '</td>',
                        '<td>', this.PackageName, '</td>',
                        '<td>', this.NextUpdateTime, '</td>',
                        '<td>', this.all_num, '</td>',
                        '<td>', this.ava_num, '</td>',
                        '<td ', 'class="', (this.Percentage >=60 ? 'text-navy' : 'text-warning'), '"',
                        '>', this.Percentage,
                        '</td>',
                        '<td>','','</td>',
                        '</tr>'
                    ].join('');
                } else {
                    var bt_id = ('bt'+i);
                    tbButtonID.push(bt_id);
                    this.td= [
                        '<tr>',
                        '<td>', (i+1), '</td>',
                        '<td>', this.PackageName, '</td>',
                        '<td>', this.NextUpdateTime, '</td>',
                        '<td>', this.all_num, '</td>',
                        '<td>', this.ava_num, '</td>',
                        '<td ', 'class="',
                        (this.Percentage >=60 ? 'text-navy' : 'text-warning'),
                        '"', '>', this.Percentage, '</td>',
                        '<td>','<button type="button" ' +
                        'class="btn btn-sm btn-primary pull-right m-t-n-xs"',
                        'id="', bt_id,'"','>','点击查询流量',
                        '<span class="glyphicon glyphicon-search" aria-hidden="true"></span>', '</button>',
                        '</td>',
                        '</tr>'
                    ].join('');
                }
            };
            this.TableMake();
            return this.td
        }).call(table_data[i], i);
        tbHTML += td_i;
    }
    // remove old form html
    table_id.simPackage.children().remove();
    // append new form html
    table_id.simPackage.append(tbHTML);
    //
    addTableButtonAction(table_data,tbButtonID);
}
function ButtonAction(bt_id, bt_num) {
    this.btID=bt_id;
    this.btNum=bt_num;
}
ButtonAction.prototype.BTClick = function (get__row_package_data) {
    this.btID.click(function () {
        console.log(get__row_package_data.NextUpdateTime);
    });
};
function addTableButtonAction(table_data, bt_list_id) {
    if (bt_list_id){
        for (var i = 0; i < bt_list_id.length; i++){
            var bt_num = Number((bt_list_id[i]).slice(2));
            new ButtonAction($(["#",bt_list_id[i]].join('')), bt_num).BTClick(table_data[bt_num]);
        }
    }
}
function getPackageInfoAjax(option_data, option_id, ajax_set) {

    var country = option_data.Country;
    var packageTypeName = option_data.PackageTypeName;
    var alertClass = 'warning';

    if (!country){
        alert_str = ['查询国家未设置，', '请选择需要查询的国家！'].join(' ');
        appendAlertInfo(alertClass, alert_str, option_id.Warn);
    } else if(!packageTypeName){
        alert_str = ['查询套餐未设置，', '请选输入要查询的套餐名！'].join(' ');
        appendAlertInfo(alertClass, alert_str, option_id.Warn);
    } else {
        var Notification = new Notificationbar(
            option_id.Notification,
            option_id.NotificationContainer,
            3000,
            false,
            option_id.NotificationContent
        );
        //
        Notification.init();
        //隐藏上次通知
        Notification.notificationAction('closeLast');
        option_id.TableSimPackage.simPackage.children().remove();
        var ajaxOption = {
            ajaxParam: {
                type: ajax_set.type,
                url: ajax_set.url,
                postData: ajax_set.data
            },
            idTag: {
                id_Alert: option_id.Warn,
                id_GetDataBt: option_id.DataGetButtonAjax,
                idTableSimPackage: option_id.TableSimPackage
            },
            objClass: {
                objNotification: Notification
            }
        };
        var packageInfoAjax = new AjaxFunc(ajaxOption.ajaxParam);
        var notifi_content = ['<strong>', '查询信息：', country, '。  数据获取中......', '</strong>'].join('');
        Notification.notificationContent(notifi_content);
        Notification.notificationAction('open');
        option_id.DataGetButtonAjax.attr("disabled", true);
        var packageInfoData = packageInfoAjax.GetAjax({idTag: ajaxOption.idTag, objClass: ajaxOption.objClass});
    }
    return false;
}
//main-初始化主程序
$(function () {
    var globParam = {
        class: {
            selectCountryCL: $(".select-country"),
            selectOrgCL: $(".select-org"),
            selectSimTypeCL: $(".form-sim-type")
        },
        id: {
            getSimPackageID: $("#id-get-sim-package-info"),
            countrySelectID: $("#id-select-country"),
            orgSelectID: $("#id-select-org"),
            simTypeSelectID: $("#id-select-sim-type"),
            packageTypeNameInputID: $("#id-package-type-name"),
            warnFirLayerID: $("#id-warn-fir-layer"),
            notificationFirID: $("#id-notification-fir"),
            notificationContentFirID: $("#id-notification-content-fir"),
            notificationContainerFirID: $("#id-notification-container-fir"),
            tableSimPackageID: $("#id-package-table"),
            avaStatusID: $("#id-ava-status"),
            businessStatusID: $("#id-business-status"),
            packageStatusID: $("#id-package-status"),
            slotStatusID: $("#id-slot-status"),
            bamStatusID: $("#id-bam-status")
        }
    };
    //select 下拉列表筛选数据-国家：
    var country_data = [{text: 'AD'}, {text: 'AE'}, {text: 'AF'}, {text: 'AG'}, {text: 'AI'}, {text: 'AL'}, {text: 'AM'}, {text: 'AO'}, {text: 'AQ'}, {text: 'AR'}, {text: 'AS'}, {text: 'AT'}, {text: 'AU'}, {text: 'AW'}, {text: 'AX'}, {text: 'AZ'}, {text: 'BA'}, {text: 'BB'}, {text: 'BD'}, {text: 'BE'}, {text: 'BF'}, {text: 'BG'}, {text: 'BH'}, {text: 'BI'}, {text: 'BJ'}, {text: 'BL'}, {text: 'BM'}, {text: 'BN'}, {text: 'BO'}, {text: 'BQ'}, {text: 'BR'}, {text: 'BS'}, {text: 'BT'}, {text: 'BV'}, {text: 'BW'}, {text: 'BY'}, {text: 'BZ'}, {text: 'CA'}, {text: 'CC'}, {text: 'CD'}, {text: 'CF'}, {text: 'CG'}, {text: 'CH'}, {text: 'CI'}, {text: 'CK'}, {text: 'CL'}, {text: 'CM'}, {text: 'CN'}, {text: 'CO'}, {text: 'CR'}, {text: 'CU'}, {text: 'CV'}, {text: 'CW'}, {text: 'CX'}, {text: 'CY'}, {text: 'CZ'}, {text: 'DE'}, {text: 'DJ'}, {text: 'DK'}, {text: 'DM'}, {text: 'DO'}, {text: 'DZ'}, {text: 'EC'}, {text: 'EE'}, {text: 'EG'}, {text: 'EH'}, {text: 'ER'}, {text: 'ES'}, {text: 'ET'}, {text: 'FI'}, {text: 'FJ'}, {text: 'FK'}, {text: 'FM'}, {text: 'FO'}, {text: 'FR'}, {text: 'GA'}, {text: 'GB'}, {text: 'GD'}, {text: 'GE'}, {text: 'GF'}, {text: 'GG'}, {text: 'GH'}, {text: 'GI'}, {text: 'GL'}, {text: 'GM'}, {text: 'GN'}, {text: 'GP'}, {text: 'GQ'}, {text: 'GR'}, {text: 'GS'}, {text: 'GT'}, {text: 'GU'}, {text: 'GW'}, {text: 'GY'}, {text: 'HK'}, {text: 'HM'}, {text: 'HN'}, {text: 'HR'}, {text: 'HT'}, {text: 'HU'}, {text: 'ID'}, {text: 'IE'}, {text: 'IL'}, {text: 'IM'}, {text: 'IN'}, {text: 'IO'}, {text: 'IQ'}, {text: 'IR'}, {text: 'IS'}, {text: 'IT'}, {text: 'JE'}, {text: 'JM'}, {text: 'JO'}, {text: 'JP'}, {text: 'KE'}, {text: 'KG'}, {text: 'KH'}, {text: 'KI'}, {text: 'KM'}, {text: 'KN'}, {text: 'KP'}, {text: 'KR'}, {text: 'KW'}, {text: 'KY'}, {text: 'KZ'}, {text: 'LA'}, {text: 'LB'}, {text: 'LC'}, {text: 'LI'}, {text: 'LK'}, {text: 'LR'}, {text: 'LS'}, {text: 'LT'}, {text: 'LU'}, {text: 'LV'}, {text: 'LY'}, {text: 'MA'}, {text: 'MC'}, {text: 'MD'}, {text: 'ME'}, {text: 'MF'}, {text: 'MG'}, {text: 'MH'}, {text: 'MK'}, {text: 'ML'}, {text: 'MM'}, {text: 'MN'}, {text: 'MO'}, {text: 'MP'}, {text: 'MQ'}, {text: 'MR'}, {text: 'MS'}, {text: 'MT'}, {text: 'MU'}, {text: 'MV'}, {text: 'MW'}, {text: 'MX'}, {text: 'MY'}, {text: 'MZ'}, {text: 'NA'}, {text: 'NC'}, {text: 'NE'}, {text: 'NF'}, {text: 'NG'}, {text: 'NI'}, {text: 'NL'}, {text: 'NO'}, {text: 'NP'}, {text: 'NR'}, {text: 'NU'}, {text: 'NZ'}, {text: 'OM'}, {text: 'PA'}, {text: 'PC'}, {text: 'PE'}, {text: 'PF'}, {text: 'PG'}, {text: 'PH'}, {text: 'PK'}, {text: 'PL'}, {text: 'PM'}, {text: 'PN'}, {text: 'PR'}, {text: 'PS'}, {text: 'PT'}, {text: 'PW'}, {text: 'PY'}, {text: 'QA'}, {text: 'RE'}, {text: 'RO'}, {text: 'RS'}, {text: 'RU'}, {text: 'RW'}, {text: 'SA'}, {text: 'SB'}, {text: 'SC'}, {text: 'SD'}, {text: 'SE'}, {text: 'SG'}, {text: 'SH'}, {text: 'SI'}, {text: 'SJ'}, {text: 'SK'}, {text: 'SL'}, {text: 'SM'}, {text: 'SN'}, {text: 'SO'}, {text: 'SR'}, {text: 'ST'}, {text: 'SV'}, {text: 'SX'}, {text: 'SY'}, {text: 'SZ'}, {text: 'TC'}, {text: 'TD'}, {text: 'TF'}, {text: 'TG'}, {text: 'TH'}, {text: 'TJ'}, {text: 'TK'}, {text: 'TL'}, {text: 'TM'}, {text: 'TN'}, {text: 'TO'}, {text: 'TR'}, {text: 'TT'}, {text: 'TV'}, {text: 'TW'}, {text: 'TZ'}, {text: 'UA'}, {text: 'UG'}, {text: 'UM'}, {text: 'US'}, {text: 'UY'}, {text: 'UZ'}, {text: 'VA'}, {text: 'VC'}, {text: 'VE'}, {text: 'VG'}, {text: 'VI'}, {text: 'VN'}, {text: 'VU'}, {text: 'WF'}, {text: 'WS'}, {text: 'YE'}, {text: 'YT'}, {text: 'ZA'}, {text: 'ZM'}, {text: 'ZW'}]
    // country init
    var select2Country = new Select2FuncBase(globParam.class.selectCountryCL, country_data);
    select2Country.init();
    select2Country.set('', true);
    //select 下拉列表筛选数据-org：
    var org_name = [{text:'35ORG'}, {text:'a2network'}, {text:'CelloMobile'}, {text:'GFC_simbank'}, {text:'GLOBALWIFI'},
        {text:'北京信威'}, {text:'GWIFI'}, {text:'JETFI桔豐科技'}, {text:'LianLian'}, {text:'POCWIFI'}, {text:'TestMvno'},
        {text:'VisonData-ORG'}, {text:'YROAM'}, {text:'all'}];
    // org init and set
    var select2Org = new Select2FuncBase(globParam.class.selectOrgCL, org_name);
    select2Org.init();
    select2Org.set('GTBU', false);
    // sim type ini and set
    var sim_type_data = [{text: '本国卡'}, {text: '多国卡'}];
    var select2SimType = new Select2FuncBase(globParam.class.selectSimTypeCL, sim_type_data);
    select2SimType.init();
    select2SimType.set('多国/本国', true);
    // tooltip init
    $('[data-toggle="tooltip"]').tooltip();
    globParam.id.getSimPackageID.click( function (){
        //alert(moment(GlobeIdSet.timeStart.val()).add(moment().utcOffset(),'m').unix());
        var option = {
            data:{
                Country: globParam.id.countrySelectID.val(),
                PackageTypeName : globParam.id.packageTypeNameInputID.val()
            },
            id:{
                Notification: globParam.id.notificationFirID,
                NotificationContent: globParam.id.notificationContentFirID,
                NotificationContainer: globParam.id.notificationContainerFirID,
                Warn: globParam.id.warnFirLayerID,
                DataGetButtonAjax: globParam.id.getSimPackageID,
                TableSimPackage: {
                    simPackage:globParam.id.tableSimPackageID
                }
            },
            ajaxSet:{
                type: 'GET',
                url: $SCRIPT_ROOT + "/api/v1.0/get_package_flower/",
                data: {
                    Country: globParam.id.countrySelectID.val(),
                    Org: globParam.id.orgSelectID.val(),
                    SimType : globParam.id.simTypeSelectID.val() ?
                        ((globParam.id.simTypeSelectID.val() === '本国卡') ? '0' : '1') : '',
                    PackageTypeName : globParam.id.packageTypeNameInputID.val()
                }
            }
        };
        getPackageInfoAjax(option.data, option.id, option.ajaxSet);
    });
});