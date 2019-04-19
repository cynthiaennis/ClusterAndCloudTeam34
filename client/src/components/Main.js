
import React, { Component } from 'react'
import Footer from './Footer'
import Header from './Header'
import HomePage from './Home'
import AboutPage from './About'
import MapPage from './Map'
import { Switch, Route, Redirect } from 'react-router-dom'
export default class Main extends Component {
  render() {
    return (
      <div>
        <Header />

        <Switch>
          <Route path="/home" component={HomePage} exact />
          {/* <Route path="/home" component={HomePage} />
          <Route
            exact
            path="/menu"
            component={() => <Menu dishes={this.state.dishes} />}
          />
          <Route path="/menu/:dishId" component={this.DishWithId} />
          <Route exact path="/contactus" component={Contact} /> */}
          <Route path="/aboutus" component={AboutPage} exact />
          <Route path="/map" component={MapPage} exact />
          {/* Default route */}
          {/* <Redirect to="/home" /> */}
        </Switch>
        <Footer />
      </div>
    )
  }
}
