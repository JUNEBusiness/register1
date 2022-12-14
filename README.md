# REGISTER ROUTE
#### Description:
This route takes in a user data from the form using POST method. Fields required include "companyName" (abbreviation of company name), "companyLegalName" (full name of company), "username", "password", "phoneNumber" and "email". The email, phone number, company name and username are unique and can not be used to register more than once. They must be sent to the api "/register" in json format.

It also contains email validations and validation methods for other data to avoid submitting empty form or invalid emails.

If data has been created successfully it will return {"message":"your account has been created successfully!"}
If an error occurs, it returns {"errorMessage":<message>}
