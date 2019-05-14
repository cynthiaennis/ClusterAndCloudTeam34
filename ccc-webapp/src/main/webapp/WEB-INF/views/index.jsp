<%@ taglib uri="http://tiles.apache.org/tags-tiles" prefix="tiles" %>
<tiles:insertDefinition name="defaultTemplate">
    <%--<tiles:putAttribute name="current" value="current"></tiles:putAttribute>--%>
    <tiles:putAttribute name="body">
        <div class="content">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-md-4">
                        <div class="card card-stats">
                            <div class="card-header card-header-info card-header-icon">
                                <div class="card-icon">
                                    <i class="fa fa-twitter"></i>
                                </div>
                                <p class="card-category">Total Tweets</p>
                                <h3 class="card-title" id="tTweets"></h3>
                            </div>
                            <div class="card-footer">
                                <div class="stats">
                                    <i class="material-icons">update</i> Just Updated
                                </div>
                            </div>
                        </div>
                        <div class="card card-stats">
                            <div class="card-header card-header-info card-header-icon">
                                <div class="card-icon">
                                    <i class="fa fa-twitter"></i>
                                </div>
                                <p class="card-category">Total Negative Tweets</p>
                                <h3 class="card-title" id="tNegative"></h3>
                            </div>
                            <div class="card-footer">
                                <div class="stats">
                                    <i class="material-icons">update</i> Just Updated
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card">
                            <div class="card-header card-header-primary">
                                <h4 class="card-title">Tweets Percentage</h4>
                                <p class="card-category">Negative sentiment vs total number of tweets</p>
                            </div>
                            <div class="card-body">
                                <div class="ct-chart" id="tweetPieChart"></div>
                            </div>
                        </div>

                        <%--<div class="card card-chart">--%>
                            <%--<div class="card-header card-header-warning">--%>
                                <%--<div class="ct-chart ct-square" id="tweetPieChart"></div>--%>
                            <%--</div>--%>
                            <%--<div class="card-body">--%>
                                <%--<h4 class="card-title">Number of Tweets </h4>--%>
                                <%--<p class="card-category">--%>
                                    <%--Total negative sentiment compare to total number of tweets</p>--%>
                            <%--</div>--%>
                            <%--<div class="card-footer">--%>
                                <%--<div class="stats">--%>
                                    <%--<i class="material-icons">access_time</i> Political sentiment tweets--%>
                                <%--</div>--%>
                            <%--</div>--%>
                        <%--</div>--%>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-header card-header-primary">
                                <h4 class="card-title">Negative Tweets</h4>
                                <p class="card-category">Chart of the political negative sentiment tweets</p>
                            </div>
                            <div class="card-body">
                                <div class="ct-chart" id="negativeTweetChart"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </tiles:putAttribute>

    <tiles:putAttribute name="pagejs">
        <link href="${pageContext.request.contextPath}/assets/css/chartist-plugin-tooltip.css" type="text/css"
              rel="stylesheet">
        </link>
        <script src="${pageContext.request.contextPath}/assets/js/plugins/chartist-plugin-tooltip.min.js"></script>
        <script type="text/javascript">
            $(document).ready(function () {
                md.initDashboardPageCharts();
            });
        </script>
    </tiles:putAttribute>
</tiles:insertDefinition>
