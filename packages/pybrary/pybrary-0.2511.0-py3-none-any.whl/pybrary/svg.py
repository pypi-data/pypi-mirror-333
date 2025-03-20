from xml.etree.ElementTree import Element as eElement, tostring


class Element:
    def __init__(self, name, **k):
        self.element = eElement(name, **k)

    def add(self, e, **k):
        if not isinstance(e, Element):
            e = Element(e, **k)
        self.element.append(e.element)
        return e

    def __setattr__(self, name, value):
        if name == 'element':
            object.__setattr__(self, name, value)
        else:
            setattr(self.element, name, value)

    def __str__(self):
        return tostring(self.element).decode()


class SVG:
    def __init__(self, **k):
        k['xmlns'] = 'http://www.w3.org/2000/svg'
        k['version'] = '1.1'
        self.root = Element('svg', **k)
        self.add = self.root.add

    def save_svg(self, name):
        with open(f'{name}.svg', 'w') as f:
            f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
            f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
            f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
            f.write(str(self))

    def save_html(self, name):
        with open(f'{name}.html', 'w') as f:
            f.write('<html><body>')
            f.write(str(self))
            f.write('</body><html>')

    def __str__(self):
        return f'{self.root}'


def test():
    svg = SVG()
    text = Element('text', x='75', y='75', fill='green')
    text.text = 'Green Text'
    svg.add(text)
    line = svg.add('line',
        x1='50',y1='50',x2='100',y2='100',
        style='stroke:rgb(255,0,0);stroke-width:3',
    )
    print(line)
    print(svg)
    svg.save_svg('test')
    svg.save_html('test')


if __name__=='__main__': test()
