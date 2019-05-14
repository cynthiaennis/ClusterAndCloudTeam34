package com.team34.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

@Controller
public class MenuController {

    @RequestMapping(value = {"/", "index"}, method = RequestMethod.GET)
    public String index(Model model) throws Exception {
        model.addAttribute("pageTitle", "Dashboard");
        return "index";
    }

    @RequestMapping(value = "maps", method = RequestMethod.GET)
    public String maps(Model model) throws Exception {
        model.addAttribute("pageTitle", "Map Analysis");
        return "maps";
    }

    @RequestMapping(value = "teammember", method = RequestMethod.GET)
    public String teamMember(Model model) throws Exception {
        model.addAttribute("pageTitle", "Team Member");
        return "teammember";
    }
}
