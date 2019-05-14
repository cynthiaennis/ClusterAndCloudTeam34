<%@taglib uri="http://tiles.apache.org/tags-tiles" prefix="tiles" %>
<!DOCTYPE html>
<!--[if IE 8]> <html lang="en" class="ie8 no-js"> <![endif]-->
<!--[if IE 9]> <html lang="en" class="ie9 no-js"> <![endif]-->
<!--[if !IE]><!-->
<html lang="en">
<!--<![endif]-->
<head>
    <meta charset="utf-8"/>
    <title>SISMIPPO | ${pageTitle}</title>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="width=device-width, initial-scale=1" name="viewport"/>
    <meta content="Direktorat Jenderal Pajak" name="author"/>
    <tiles:insertAttribute name="mandatorystyle"></tiles:insertAttribute>
    <tiles:insertAttribute name="pagecss" ignore="true"></tiles:insertAttribute>
    <link rel="shortcut icon"
          href="${pageContext.request.contextPath}/assets/pages/img/IconKemenkeu.ico"/>
    <script type="text/javascript">
        var ctx = "${pageContext.request.contextPath}";
    </script>
</head>
<body class="page-container-bg-solid page-header-fixed page-sidebar-closed-hide-logo">
<tiles:insertAttribute name="header"></tiles:insertAttribute>
<div class="clearfix"></div>
<div class="page-container">
    <tiles:insertAttribute name="sidebar"></tiles:insertAttribute>
    <div class="page-content-wrapper">
        <div class="page-content">
            <tiles:insertAttribute name="breadcrumb"></tiles:insertAttribute>
            <tiles:insertAttribute name="body"></tiles:insertAttribute>
        </div>
    </div>
    <tiles:insertAttribute name="footer"></tiles:insertAttribute>

</div>
<tiles:insertAttribute name="mandatoryscript"></tiles:insertAttribute>
<tiles:insertAttribute name="pagejs" ignore="true"></tiles:insertAttribute>
</body>
</html>