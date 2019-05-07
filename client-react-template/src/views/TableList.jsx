import React, {Component} from "react";
import {Grid, Row, Col, Table} from "react-bootstrap";

import Card from "components/Card/Card.jsx";
import {thArray, tdArray} from "variables/Variables.jsx";

//import app from 'app.js';

// const nano = require('nano')('http://localhost:5984');
// const customers = nano.db.use('customers');
// customers.view('all_customers', 'all')
//     .then((body) => {
//         body.rows.forEach((doc) => {
//             console.log(doc.value);
//         });
//     });

class TableList extends React.Component {
    constructor() {
        super();
        this.state = { data: [] };
    }
    componentDidMount() {
        const nano = require('nano')('http://localhost:5984');
        const customers = nano.db.use('customers');
        customers.view('all_customers', 'all')
            .then((body) => this.setState({data:body}));
            //.then(json => this.setState({data:json}));

        // fetch(`http://localhost:5984/_utils/index.html#/database/customers/_design/all_customers/_view/all`)
        //     .then(res => res.json())
        //     .then(json => this.setState({ data: json }));
    }
    // componentDidMount() {
    //     const nano = require('nano')('http://localhost:5984');
    //     const customers = nano.db.use('customers');
    //     const newState = Object.assign({}, this.state, {
    //         customers: customers.view('all_customers', 'all')
    //     });
    //
    //     this.setState(newState);
    // }

    render() {
        return (
            <div className="content">
                <Grid fluid>
                    <Row>
                        <Col md={12}>
                            <Card
                                title="Striped Table with Hover"
                                category="Here is a subtitle for this table"
                                ctTableFullWidth
                                ctTableResponsive
                                content={
                                    <Table striped hover>
                                        <thead>
                                        <tr>
                                            {this.state.data.map((prop, key) => {
                                                return <th key={key}>{prop}</th>;
                                            })}
                                        </tr>
                                        </thead>
                                        <tbody>
                                        {this.state.data.map((prop, key) => {
                                            return (
                                                <tr key={key}>
                                                    {prop.map((prop, key) => {
                                                        return <td key={key}>{prop}</td>;
                                                    })}
                                                </tr>
                                            );
                                        })}
                                        </tbody>
                                    </Table>
                                }
                            />
                        </Col>

                        {/* <Col md={12}>
              <Card
                plain
                title="Striped Table with Hover"
                category="Here is a subtitle for this table"
                ctTableFullWidth
                ctTableResponsive
                content={
                  <Table hover>
                    <thead>
                      <tr>
                        {thArray.map((prop, key) => {
                          return <th key={key}>{prop}</th>;
                        })}
                      </tr>
                    </thead>
                    <tbody>
                      {tdArray.map((prop, key) => {
                        return (
                          <tr key={key}>
                            {prop.map((prop, key) => {
                              return <td key={key}>{prop}</td>;
                            })}
                          </tr>
                        );
                      })}
                    </tbody>
                  </Table>
                }
              />
            </Col>*/}
                    </Row>
                </Grid>
            </div>
        );
    }
}

export default TableList;
