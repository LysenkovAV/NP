## NP

This is a news portal with the following features for participants:
* registration on the portal;
* become an author;
* search for posts by various parameters;
* subscribe to categories and receive newsletters.

## Examples

| Path                       | Description                                                  |
| -------------------------- | ------------------------------------------------------------ | 
| .../                       | the author's page with a redirect to authorization           |
| .../accounts/login         | authorization and registration                               |
| .../news                   | list of posts                                                |
| .../news/<_id_>            | post by id                                                   |
| .../news/create            | create post                                                  |
| .../news/<_id_>/edit       | edit post                                                    |
| .../news/<_id_>/delete     | delete post                                                  |
| .../news/categories/<_id_> | category by id                                               |