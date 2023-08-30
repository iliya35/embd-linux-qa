// npx cypress run --spec cypress/e2e/webapp.cy.js --headed --browser chrome

describe('webapp Tests', () => 
{
    const baseUrl = "http://localhost:8181/";
    const username = "user";
    const password = "password";

    beforeEach(() => {
        cy.visitTab(""); // Go to main page
    })

    it('webapp_available', function() {
        cy.request({
            url: baseUrl,
            failOnStatusCode: false // Allows you to get a status code even in case of failure
        }).then((response) => {
            expect(response.status).to.eq(200); // Check status code
        });
    })

    it('webapp_title', function() {
        cy.visitTab("#en:status");
        cy.title().should('eq', 'Customer webapp');
        //   expect(true).to.equal(true)
    })

    it('Should successfully log in with valid credentials', () => {
        // Before login
        cy.request({
            method: 'GET',
            url: 'http://localhost:8181/system',
            failOnStatusCode: false
        }).then((response) => {
            // Check that the response code is ERR_HTTP_RESPONSE_CODE_FAILURE
            expect(response.status).to.eq(401);
        });
        cy.visitTab("#en:status");
    
        // Enter valid username and password
        cy.get('input[name="user"]').type(username);
        cy.get('input[name="password"]').type(password);
    
        // Click the login button
        cy.get('button[type="submit"]').click();
        cy.wait(3000); 
    
         // After login
        cy.request('http://localhost:8181/system').then((loggedInResponse) => {
            // Check that the response code is 200
            expect(loggedInResponse.status).to.eq(200); 
        });

      });
}
)