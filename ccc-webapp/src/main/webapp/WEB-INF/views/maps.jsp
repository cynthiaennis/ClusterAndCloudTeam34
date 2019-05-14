<%@ taglib uri="http://tiles.apache.org/tags-tiles" prefix="tiles" %>
<tiles:insertDefinition name="defaultTemplate">
    <%--<tiles:putAttribute name="current" value="current"></tiles:putAttribute>--%>
    <tiles:putAttribute name="body">
        <div id="map"></div>
    </tiles:putAttribute>

    <tiles:putAttribute name="pagejs">
        <!--  Google Maps Plugin    -->
        <script src="https://maps.googleapis.com/maps/api/js?key="></script>
        <script src="${pageContext.request.contextPath}/assets/demo/maps.js"></script>
    </tiles:putAttribute>
</tiles:insertDefinition>
