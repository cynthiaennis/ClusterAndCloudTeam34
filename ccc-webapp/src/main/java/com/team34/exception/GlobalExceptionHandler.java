package com.team34.exception;


import com.team34.model.ExceptionModel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.servlet.NoHandlerFoundException;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@ControllerAdvice
@EnableWebMvc
public class GlobalExceptionHandler {
    public static final Logger LOGGER = LoggerFactory.getLogger(GlobalExceptionHandler.class);

  /*  @ExceptionHandler(NoHandlerFoundException.class)
    public ResponseEntity<Error> handle(NoHandlerFoundException ex) {
        String message = "HTTP " + ex.getHttpMethod() + " for " + ex.getRequestURL() + " is not supported.";
        Error error = new Error(HttpStatus.NOT_FOUND.value(), message);
        return new ResponseEntity<Error>(error, HttpStatus.NOT_FOUND);
    }*/

    @ExceptionHandler(NoHandlerFoundException.class)
    public String handleNotFound(NoHandlerFoundException ex, Model model) {
        model.addAttribute("pageTitle", "404");
        model.addAttribute("link",  ex.getRequestURL());
        return "error/404";
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ExceptionModel> handle(Exception ex, HttpServletRequest request,
                                                 HttpServletResponse response) {
        ExceptionModel exceptionModel = new ExceptionModel();

        if (ex instanceof NullPointerException) {
            exceptionModel.setCode( HttpStatus.BAD_REQUEST.toString());
            exceptionModel.setMessage(ex.getMessage());
            return new ResponseEntity<ExceptionModel>(exceptionModel, HttpStatus.BAD_REQUEST);
        }
        else {
            exceptionModel.setCode( HttpStatus.INTERNAL_SERVER_ERROR.toString());
            exceptionModel.setMessage(ex.getMessage());
            return new ResponseEntity<ExceptionModel>(exceptionModel, HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
