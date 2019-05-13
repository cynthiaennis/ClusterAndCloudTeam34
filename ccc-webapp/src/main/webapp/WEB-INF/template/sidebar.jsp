<div class="sidebar" data-color="azure" data-background-color="white"
     data-image="${pageContext.request.contextPath}/assets/img/sidebar-3.jpg">
    <!--
      Tip 1: You can change the color of the sidebar using: data-color="purple | azure | green | orange | danger"

      Tip 2: you can also add an image using data-image tag
  -->
    <div class="logo">
        <a href="javascript:void(0);" class="simple-text logo-normal">
            Team 34
        </a>
    </div>
    <div class="sidebar-wrapper">
        <ul class="nav">
            <li class="nav-item active  ">
                <a class="nav-link" href="${pageContext.request.contextPath}/index">
                    <i class="material-icons">dashboard</i>
                    <p>Dashboard</p>
                </a>
            </li>
            <li class="nav-item ">
                <a class="nav-link" href="${pageContext.request.contextPath}/maps">
                    <i class="material-icons">location_ons</i>
                    <p>Maps</p>
                </a>
            </li>
            <li class="nav-item ">
                <a class="nav-link" href="${pageContext.request.contextPath}/teammember">
                    <i class="material-icons">person</i>
                    <p>Team Member</p>
                </a>
            </li>
        </ul>
    </div>
</div>
