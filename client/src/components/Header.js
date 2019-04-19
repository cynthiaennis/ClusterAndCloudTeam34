
import React, { Component } from 'react'
import { Nav } from 'react-bootstrap';
import GoogleFontLoader from 'react-google-font-loader';


export default class Header extends Component {
  render() {
    return (


      <div className='navbar'>
        <GoogleFontLoader
          fonts={[
            {
              font: 'Roboto',
              weights: [400, '400i'],
            },
            {
              font: 'Roboto Mono',
              weights: [400, 700],
            },
          ]}
          subsets={['cyrillic-ext', 'greek']}
        />

        <p className="text-center mt-4 mb-4 mr-5 logo" style={{ fontFamily: 'Roboto Mono, monospaced' }}>COMP90024 Cluster and cloud computing team 34</p>
        <Nav className="justify-content-center">

          <Nav.Item>
            <Nav.Link href="/home"  className='nav-link'>Home</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href='/aboutus' className='nav-link'>About</Nav.Link>
          </Nav.Item>
          <Nav.Item>
            <Nav.Link href='/map' className='nav-link'>Map</Nav.Link>
          </Nav.Item>
          
        </Nav>
      </div>
    )
  }
}
