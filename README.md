# Volair | Self-Driven Autonomous Python Libraries

The Volair is designed to help data scientists and ML engineers efficiently manage and automate maintenance-free utility library creation. It provides a simple, easy-to-use Python interface to interact with the Volair platform.



## Features

- Easy serialization of functions and classes, making them readily available for reuse across different projects.
- Automatic documentation generation for effortless maintenance and readability.
- Support for both direct and modular function importation from the library.
- Streamlined version control and collaboration features, allowing teams to work together seamlessly.

### Easiest Library View
Usponic proveides an dashboard for your team members. After the accessing they can easily view the top libraries and automaticaly generated connections codes.


### Automaticaly Documentation
In Volair On-Prem dashboard we have automaticaly generated documentation for your each function, class, object or variables. For this you can use OpenAI GPT integration or a self-hosted Google Gemma model in your installation. They are making your documentations automaticaly. Also you can easily search your content.

- Documentation
- Time Complexity
- Mistakes
- Required Test Tyoes
- Security Analyses
- Tags

## Installation

You need to install the Volair container.

Once the container is up and running, you can install the Volair Python Client Library on your local system using the pip package manager:
```console
# pip install volair
```



## Usage

Here's an updated quickstart guide to get you up and running with your container:

```python
from volair import VolairOnPrem
volair = VolairOnPrem('https://your-server-address:5000', 'ACK_****************')



def sum(a, b):
    return a + b

volair.dump("math.basics.sum", sum)



math = volair.load_module("math")

math.basics.sum(5, 2)
```



## Contributing

We welcome contributions to the Volair Python Client Library! 



## Support & Questions

For any questions or if you encounter an issue, please reach out to our support team at volairlabs@gmail.com or open an issue on the project's GitHub page.
