import React from 'react'
import { Container, Row, Col, Image } from 'react-bootstrap'
export default function AboutPage() {
  return (
    <Container>
      <h2 className="mt-3">Team members</h2>

      <hr />

      <Container className='member-info'>


        {/* Stack the columns on mobile by making one full-width and the other half-width */}
        <Row>
          <Col xs={12} sm={4} className='picture-holer text-center'>
            <h5>Cynthia Maree Ennis</h5>
            <Image src="https://via.placeholder.com/150" className="rounded mb-3" />
            <hv />
          </Col>
          <Col xs={12} sm={8}>
            <h5>Info Heading</h5>
            <p>
              Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque
              ante sollicitudin commodo. Cras purus odio, vestibulum in vulputate at,
              tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate
              fringilla. Donec lacinia congue felis in faucibus.
            </p>

            <p>
              Donec sed odio dui. Nullam quis risus eget urna mollis ornare vel eu
              leo. Cum sociis natoque penatibus et magnis dis parturient montes,
              nascetur ridiculus mus.
            </p>
          </Col>
        </Row>

        <Row>
          <Col xs={12} sm={4} className='picture-holer text-center'>
            <h5>Jane Ho</h5>
            <Image src="https://via.placeholder.com/150" className="rounded mb-3" />
            <hv />
          </Col>
          <Col xs={12} sm={8}>
            <h5>Info Heading</h5>
            <p>
              Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque
              ante sollicitudin commodo. Cras purus odio, vestibulum in vulputate at,
              tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate
              fringilla. Donec lacinia congue felis in faucibus.
            </p>

            <p>
              Donec sed odio dui. Nullam quis risus eget urna mollis ornare vel eu
              leo. Cum sociis natoque penatibus et magnis dis parturient montes,
              nascetur ridiculus mus.
            </p>
          </Col>
        </Row>

        <Row>
          <Col xs={12} sm={4} className='picture-holer text-center'>
            <h5>Yen-Peng Chen</h5>
            <Image src="https://via.placeholder.com/150" className="rounded mb-3" />
            <hv />
          </Col>
          <Col xs={12} sm={8}>
            <h5>Info Heading</h5>
            <p>
              Cras sit amet nibh libero, in gravida nulla. Nulla vel metus scelerisque
              ante sollicitudin commodo. Cras purus odio, vestibulum in vulputate at,
              tempus viverra turpis. Fusce condimentum nunc ac nisi vulputate
              fringilla. Donec lacinia congue felis in faucibus.
            </p>

            <p>
              Donec sed odio dui. Nullam quis risus eget urna mollis ornare vel eu
              leo. Cum sociis natoque penatibus et magnis dis parturient montes,
              nascetur ridiculus mus.
            </p>
          </Col>
        </Row>


      </Container>;

      </Container>
  )
}
